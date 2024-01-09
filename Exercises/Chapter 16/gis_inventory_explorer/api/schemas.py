from pydantic import BaseModel
from typing import Optional

class UserIn(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    email: str
    is_active: bool


class TokenData(BaseModel):
    email: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
