import threading
import time
from typing import List

from fastapi import APIRouter, Depends
from fastapi import HTTPException

from api.account.schemas import TokenResponseSchema, AccountSchema, Signin
from api.record.schemas import AccountCreds, RecordResponse, AccountVerification,AccountDriver
from common.enums import EntryStatus
from helpers.common import get_mac_chrome_driver
from helpers.deps import Auth
from helpers.insta_process import login_and_verify, login_2fa, login_challenge, scrape_followers, add_to_close_friends
from helpers.jwt import create_access_token
from model import Account
from selenium import webdriver
from typing import Dict

router = APIRouter()
driver_sessions: Dict[str, webdriver.Chrome] = {}




@router.get('',response_model=List[RecordResponse])
def get_all_records(account: Account = Depends(Auth())):
    data = []

    for each in account.records:
        # Passed = 0
        # Failed = 0

        pass_count = len([x for x in each.record.record_entries if x.entry.status == EntryStatus.Passed.value])
        fail_count = each.record.followers - pass_count
        record_data = {"username": each.record.username,
         "status":each.record.status,
         "followers":each.record.followers,
         "fail_count":fail_count,
         "pass_count": pass_count}
        data.append(record_data)

    return data


from fastapi import APIRouter, HTTPException, Depends
from selenium import webdriver
from typing import Dict
from pydantic import BaseModel

router = APIRouter()
driver_sessions: Dict[str, webdriver.Chrome] = {}



@router.post('/login')
def login_account(data: AccountCreds):
    driver = get_mac_chrome_driver()
    driver_sessions[data.session_id] = driver
    value = login_and_verify(driver, data.username, data.password)
    return {"status": "success", "value": value}

@router.post('/code')
def login_account_code(data : AccountVerification):
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


def process_followers(driver, username):
    """
    Function to scrape followers and add them to close friends in a separate thread.
    """
    try:
        followers = scrape_followers(driver, username)
        print(f"Total followers: {len(followers)}")
        for each in followers:
            time.sleep(1)  # Simulate processing delay
            try:
                add_to_close_friends(driver, each)
            except:
                print(f"skipped = {each}")
        driver.quit()
    except Exception as e:
        driver.quit()
        print(f"Error in processing followers: {e}")
@router.post('/start_process')
def login_account_code(data : AccountDriver):
    try:
        driver = driver_sessions.get(data.session_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Session not found.")
        background_thread = threading.Thread(
            target=process_followers, args=(driver, data.username), daemon=True
        )
        background_thread.start()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")
    return {"status": "verification success"}