from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TextdataSchema(BaseModel):
    id: int
    hashid: str
    line_number: int
    text: str
    timestamp: datetime

    class Config:
        orm_mode: True

class TypewriterSchema(BaseModel):
    id: int
    uuid: str
    user_firstname: Optional[str] = None
    user_lastname: Optional[str] = None
    user_email: str
    chat_active: bool
    erika_name: str
    email: str
    status: int


class MessageSchema(BaseModel):
    id: int
    typewriter: TypewriterSchema
    sender: str
    subject: str
    body: str
    timestamp: datetime
    is_printed: bool

    class Config:
        orm_mode: True

class TypewriterCreateSchema(BaseModel):
    uuid: str
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: str
    chat_active: bool = True
    erika_name: str
