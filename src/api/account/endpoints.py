import logging

from fastapi import APIRouter, Depends
from fastapi import HTTPException

from api.account.schemas import TokenResponseSchema, AccountSchema, Signin
from helpers.deps import Auth
from helpers.jwt import create_access_token
from model import Account

router = APIRouter()

@router.post("/create", response_model=TokenResponseSchema)
def create_account (account: AccountSchema):
    if Account.get_by_username(username=account.username) or Account.get_by_email(account.email):
        raise HTTPException(status_code=400, detail="Already Exist.")
    else:
        account = Account(username=account.username,email=account.email,status=True,password=account.password)
        account.insert()
        access, refresh = create_access_token(account.id)
        token = {
            "full_name": account.username,
            "access_token": access,
            "refresh_token": refresh,
            "email": account.email
        }
        return token


# Get all roles


# Get a role by ID

@router.post('/signin')
def signin(creds : Signin):
    account = Account.sign_in(creds.username,creds.password)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")
    access, refresh = create_access_token(account.id)
    token = {
        "full_name": account.username,
        "access_token": access,
        "refresh_token": refresh,
        "email": account.email
    }
    return token


@router.get('/test')
def test(account: Account = Depends(Auth())):
    logging.info("in Info")
    logging.debug("in Info")
    logging.error("in Info")
    logging.exception("in Info")