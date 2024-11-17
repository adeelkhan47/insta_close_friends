from typing import List

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

class Signin(BaseModel):

    username: str
    password : str
