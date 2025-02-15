from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str


class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str