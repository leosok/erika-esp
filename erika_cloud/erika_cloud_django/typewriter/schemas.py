from pydantic import BaseModel, Field
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
    user_firstname: str | None = None
    user_lastname: str | None = None
    user_email: str
    chat_active: bool
    erika_name: str
    email: str
    status: int

    class Config:
        from_attributes = True  # newer way to specify orm_mode

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

class PageLineSchema(BaseModel):
    line_number: int
    text: str
    timestamp: datetime

    class Config:
        orm_mode = True

class PageSchema(BaseModel):
    hashid: str
    lines: List[PageLineSchema]
    created_at: datetime
    is_printed: bool = False

    class Config:
        orm_mode = True
