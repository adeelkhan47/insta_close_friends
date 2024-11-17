from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from helpers.jwt import decode_token
from helpers.response import error
from model.account import Account


class Auth(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(Auth, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(Auth, self).__call__(
            request
        )
        if credentials:
            if not credentials.scheme == "Bearer":
                raise error("Invalid authentication scheme.", code=403)
            account_id, message = decode_token(credentials.credentials)
            if account_id is None:
                raise error(message, code=401)
            account = Account.get_by_id(account_id)
            if not account:
                raise error("User not found", code=401)
            return account
        raise error("Invalid authorization code.", code=401)
