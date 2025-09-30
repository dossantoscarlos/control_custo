from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    error: Optional[str] = None
    error_description: Optional[str] = None
    
class LoginRequest(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: str
    username: str
    email: str
    roles: list[str]
