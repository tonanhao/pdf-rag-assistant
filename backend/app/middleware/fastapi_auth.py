# backend/app/middleware/fastapi_auth.py
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, InvalidSignatureError
import os
from typing import Optional

# JWT settings (should match auth API service)
JWT_SECRET = os.getenv('SECRET_KEY', 'JWT_SECRET_KEY')  # Match auth API config.py naming  
JWT_ALGORITHM = 'HS256'

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Verify JWT token and return user information
    """
    try:
        # Decode the JWT token
        payload = jwt.decode(
            credentials.credentials, 
            JWT_SECRET, 
            algorithms=[JWT_ALGORITHM]
        )
        
        # Extract user information
        user_id = payload.get('sub')
        email = payload.get('email')
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: user ID not found"
            )
        
        return {
            'user_id': str(user_id),
            'email': email
        }
        
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except (InvalidTokenError, InvalidSignatureError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )

def get_current_user(user_data: dict = Depends(verify_token)) -> dict:
    """
    Get current user information from JWT token
    """
    return user_data

# Optional dependency for routes that can work with or without authentication
def get_current_user_optional(credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))) -> Optional[dict]:
    """
    Get current user information from JWT token, but don't require authentication
    """
    if not credentials:
        return None
    
    try:
        payload = jwt.decode(
            credentials.credentials, 
            JWT_SECRET, 
            algorithms=[JWT_ALGORITHM]
        )
        
        user_id = payload.get('sub')
        email = payload.get('email')
        
        if not user_id:
            return None
        
        return {
            'user_id': str(user_id),
            'email': email
        }
        
    except (ExpiredSignatureError, InvalidTokenError, InvalidSignatureError):
        return None 