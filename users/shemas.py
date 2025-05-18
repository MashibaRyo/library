from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: int
    email: EmailStr
    hashed_password: int

class SUserAuth(BaseModel):
    name: str
    email: EmailStr
    hashed_password: str

