from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Union, Any
from datetime import datetime


class Message(BaseModel):
    id: Union[str, int]
    role: str
    content: str
    timestamp: Union[datetime, str]

    @field_validator('id', mode='before')
    @classmethod
    def ensure_id_string(cls, v):
        return str(v) if isinstance(v, int) else v


class Conversation(BaseModel):
    id: str
    title: str
    lastMessage: str
    timestamp: Union[datetime, str]
    messages: List[Message]
    pdf_file: Optional[str] = None


class ConversationCreate(BaseModel):
    title: str
    lastMessage: str
    messages: List[Message] = Field(default_factory=list)


class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    lastMessage: Optional[str] = None
    messages: Optional[List[Message]] = None