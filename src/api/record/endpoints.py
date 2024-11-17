from typing import List

from fastapi import APIRouter, Depends
from fastapi import HTTPException

from api.account.schemas import TokenResponseSchema, AccountSchema, Signin
from api.record.schemas import RecordResponse
from common.enums import EntryStatus
from helpers.deps import Auth
from helpers.jwt import create_access_token
from model import Account

router = APIRouter()



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