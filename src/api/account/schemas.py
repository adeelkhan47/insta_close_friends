from typing import List

from pydantic import BaseModel



class TokenResponseSchema(BaseModel):
    full_name: str
    access_token: str
    refresh_token: str
    email: str



class AccountSchema(BaseModel):

    username: str
    password : str
    email : str

class Signin(BaseModel):

    username: str
    password : str
