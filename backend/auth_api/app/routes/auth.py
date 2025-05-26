from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import timedelta
from typing import Annotated

from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.models.user import User
from app.schemas.token import Token, TokenData
from app.schemas.user import UserLogin, ForgotPassword, ResetPassword

router = APIRouter(prefix="/auth", tags=["authentication"])

# OAuth2 scheme cho việc xác thực token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
) -> User:
    """Xác thực người dùng hiện tại từ token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Không thể xác thực thông tin đăng nhập",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Giải mã token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    # Tìm người dùng trong database
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    
    # Kiểm tra trạng thái tài khoản
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản đã bị vô hiệu hóa"
        )
    
    return user

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    """API đăng nhập và nhận access token"""
    # Tìm người dùng trong database
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # Kiểm tra người dùng và mật khẩu
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Kiểm tra trạng thái tài khoản
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản đã bị vô hiệu hóa"
        )
    
    # Tạo thời gian hết hạn token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Tạo access token
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login/json", response_model=Token)
async def login_json(user_data: UserLogin, db: Session = Depends(get_db)):
    """API đăng nhập bằng JSON và nhận access token"""
    # Tìm người dùng trong database
    user = db.query(User).filter(User.email == user_data.email).first()
    
    # Kiểm tra người dùng và mật khẩu
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác"
        )
    
    # Kiểm tra trạng thái tài khoản
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản đã bị vô hiệu hóa"
        )
    
    # Tạo thời gian hết hạn token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Tạo access token
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(email_data: ForgotPassword, db: Session = Depends(get_db)):
    """API quên mật khẩu"""
    # Tìm người dùng trong database
    user = db.query(User).filter(User.email == email_data.email).first()
    
    # Luôn trả về thành công để tránh lộ thông tin người dùng
    # Trong thực tế, bạn sẽ gửi email với link đặt lại mật khẩu
    return {"message": "Nếu email tồn tại, bạn sẽ nhận được hướng dẫn đặt lại mật khẩu."}

@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(reset_data: ResetPassword, db: Session = Depends(get_db)):
    """API đặt lại mật khẩu"""
    # Kiểm tra mật khẩu xác nhận
    if reset_data.new_password != reset_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mật khẩu xác nhận không khớp"
        )
    
    # Trong thực tế, bạn sẽ xác thực token đặt lại mật khẩu và cập nhật mật khẩu mới
    
    return {"message": "Mật khẩu đã được đặt lại thành công."}
