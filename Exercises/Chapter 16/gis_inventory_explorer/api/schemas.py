from pydantic import BaseModel
from typing import Union

class UserIn(BaseModel):
    username: str
    email: str
    password: str


class UserOut(BaseModel):
    username: str
    is_active: bool


class TokenData(BaseModel):
    username: Union[str, None] = None

class Token(BaseModel):
    access_token: str
    token_type: str
