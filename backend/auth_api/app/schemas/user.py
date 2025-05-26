from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """Schema cơ bản cho thông tin người dùng"""
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    """Schema cho việc tạo người dùng mới"""
    password: str = Field(..., min_length=8)
    confirm_password: str

class UserLogin(BaseModel):
    """Schema cho việc đăng nhập"""
    email: EmailStr
    password: str

class UserResponse(UserBase):
    """Schema cho việc trả về thông tin người dùng"""
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class ForgotPassword(BaseModel):
    """Schema cho quên mật khẩu"""
    email: EmailStr

class ResetPassword(BaseModel):
    """Schema cho đặt lại mật khẩu"""
    token: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str
