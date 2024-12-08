import logging
import threading
import time
from typing import Dict
from typing import List

from fastapi import APIRouter, Depends
from selenium import webdriver

from api.record.schemas import AccountCreds, RecordResponse, AccountVerification, AccountDriver
from common.enums import EntryStatus, RecordStatus
from helpers.common import get_ubuntu_chrome_driver, get_mac_chrome_driver
from helpers.deps import Auth
from helpers.insta_process import login_and_verify, login_2fa, login_challenge, scrape_followers, add_to_close_friends
from model import Account, Record, AccountRecord, Entry, RecordEntry
from fastapi import APIRouter, HTTPException


router = APIRouter()
driver_sessions: Dict[str, webdriver.Chrome] = {}




@router.get('',response_model=List[RecordResponse])
def get_all_records(account: Account = Depends(Auth())):
    data = []

    for each in account.records:
        # Passed = 0
        # Failed = 0

        pass_count = len([x for x in each.record.record_entries if x.entry.status == EntryStatus.Passed.value])
        fail_count = len([x for x in each.record.record_entries if x.entry.status == EntryStatus.Failed.value])
        record_data = {"username": each.record.username,
         "status":each.record.status,
         "followers":each.record.followers,
         "fail_count":fail_count,
         "pass_count": pass_count}
        data.append(record_data)

    return data





@router.post('/login')
def login_account(data: AccountCreds,account: Account = Depends(Auth())):
    # driver = get_mac_chrome_driver()
    driver = get_ubuntu_chrome_driver()
    driver_sessions[data.session_id] = driver

    my_rec = [each.record for each in account.records]
    record = None
    for each in my_rec:
        if each.username == data.username:
            record = each
            break
    if not record:
        record = Record(username=data.username, status=RecordStatus.Pending.value, followers=0)
        record.insert()
        account_Record = AccountRecord(account_id=account.id, record_id=record.id)
        account_Record.insert()

    value = login_and_verify(driver, data.username, data.password)




    return {"status": "success", "value": value}

@router.post('/code')
def login_account_code(data : AccountVerification,account: Account = Depends(Auth())):
    try:
        driver = driver_sessions.get(data.session_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Session not found.")
        if data.value == 1:
            login_2fa(driver,data.code)
        elif data.value == 2:
            login_challenge(driver,data.code)
        else:
            raise HTTPException(status_code=400, detail="Invalid code type.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")
    return {"status": "verification success"}


def process_followers(driver, username,account_id):
    """
    Function to scrape followers and add them to close friends in a separate thread.
    """
    account = Account.get_by_id_with_db(account_id)
    my_rec = [each.record for each in account.records]
    record = None
    for each in my_rec:
        if each.username == username:
            record = each
    account_record = AccountRecord.get_record_by_account_and_record(account_id=account_id, record_id=record.id)
    previous_entries = [record_entries.entry.follower for record_entries in record.record_entries if record_entries.entry.status == EntryStatus.Passed.value]

    if account_record:
        try:
            Record.update(id=record.id,to_update={"status":RecordStatus.FetchingFollowers.value})
            followers = scrape_followers(driver, username,limit=500)
            Record.update(id=record.id, to_update={"followers": len(followers)})
            logging.debug(f"Total followers: {len(followers)}")
            Record.update(id=record.id, to_update={"status": RecordStatus.AddingFollowers.value})
            for each in followers:
                time.sleep(1)  # Simulate processing delay
                try:

                    if each not in previous_entries:
                        item = add_to_close_friends(driver, each)
                        if item:
                            entry = Entry(follower=each,status=EntryStatus.Passed.value)
                        else:
                            entry = Entry(follower=each, status=EntryStatus.Failed.value)
                        entry.insert()
                        record_entry = RecordEntry(record_id=record.id,entry_id=entry.id)
                        record_entry.insert()
                except:
                    logging.debug(f"skipped = {each}")
            Record.update(id=record.id, to_update={"status": RecordStatus.Success.value})
            driver.quit()
        except Exception as e:
            Record.update(id=record.id, to_update={"status": RecordStatus.Failed.value})
            driver.quit()

            logging.debug(f"Error in processing followers: {e}")
@router.post('/start_process')
def login_account_code(data : AccountDriver,account: Account = Depends(Auth())):
    try:
        driver = driver_sessions.get(data.session_id)

        if not driver:
            raise HTTPException(status_code=404, detail="Session not found.")

        # background_thread = threading.Thread(
        #     target=process_followers, args=(driver, data.username,account.id), daemon=True
        # )
        # background_thread.start()
        process_followers(driver,data.username,account_id=account.id)
        return {"status": "verification success"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")
