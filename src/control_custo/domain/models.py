from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str
    description: str | None = None


class TokenDTO(BaseModel):
    access_token: str

    
class LoginRequest(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: str
    username: str
    email: str
    roles: list[str]
