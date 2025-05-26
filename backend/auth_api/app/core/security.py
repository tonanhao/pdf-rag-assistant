from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Tạo context để mã hóa mật khẩu với các cài đặt an toàn
# Sử dụng bcrypt trực tiếp nếu gặp vấn đề với passlib
use_passlib = True
try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # Test để xem có lỗi không
    test_hash = pwd_context.hash("test_password")
    pwd_context.verify("test_password", test_hash)
except Exception:
    use_passlib = False
    print("Using bcrypt directly due to passlib compatibility issue")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Kiểm tra mật khẩu đầu vào với mật khẩu đã được hash"""
    if use_passlib:
        return pwd_context.verify(plain_password, hashed_password)
    else:
        # Sử dụng bcrypt trực tiếp
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    """Tạo mật khẩu hash từ mật khẩu gốc"""
    if use_passlib:
        return pwd_context.hash(password)
    else:
        # Sử dụng bcrypt trực tiếp
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Tạo access token JWT"""
    to_encode = data.copy()
    
    # Thiết lập thời gian hết hạn token
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Thêm thời gian hết hạn vào payload
    to_encode.update({"exp": expire})
    
    # Tạo token JWT
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt
