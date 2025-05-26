from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """Schema cho token JWT"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema cho dữ liệu được lưu trong token"""
    email: Optional[str] = None
    user_id: Optional[int] = None
