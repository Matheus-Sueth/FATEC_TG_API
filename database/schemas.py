from pydantic import BaseModel

class MessageBase(BaseModel):
    message: str
    hora: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    owner_name: str

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    nome: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    messages: list[Message] = []

    class Config:
        orm_mode = True
