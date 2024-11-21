from pydantic import BaseModel



class TokenResponseSchema(BaseModel):
    full_name: str
    access_token: str
    refresh_token: str
    email: str



class RecordResponse(BaseModel):

    username: str
    status : str
    followers : int
    fail_count : int
    pass_count : int

class AccountCreds(BaseModel):

    username: str
    password : str
    session_id: str
class AccountVerification(BaseModel):
    session_id: str
    value : int
    code: str
class AccountDriver(BaseModel):
    session_id: str
    username: str

class Signin(BaseModel):

    username: str
    password : str
