from pydantic import BaseModel, Field
from typing import List, Optional, Union, Any
from datetime import datetime
from pydantic import validator

class Message(BaseModel):
    id: Union[str, int]  # Accept both string and integer IDs
    role: str
    content: str
    timestamp: Union[datetime, str]
    
    @validator('timestamp', pre=True)
    def parse_timestamp(cls, value):
        if isinstance(value, str):
            return value  # Keep string format
        return value
    
    @validator('id', pre=True)
    def ensure_id_serializable(cls, value):
        # Ensure ID can be serialized to JSON
        return str(value) if isinstance(value, int) else value

class Conversation(BaseModel):
    id: str
    title: str
    lastMessage: str
    timestamp: Union[datetime, str]
    messages: List[Message]
    pdf_file: Optional[str] = None  # Path to the PDF file if attached
    user_id: Optional[str] = None  # User ID for user-specific conversations
    
    @validator('timestamp', pre=True)
    def parse_timestamp(cls, value):
        if isinstance(value, str):
            return value  # Keep string format
        return value

class ConversationCreate(BaseModel):
    title: str
    lastMessage: str
    messages: List[Message] = Field(default_factory=list)
    
class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    lastMessage: Optional[str] = None
    messages: Optional[List[Message]] = None 