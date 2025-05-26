#!/usr/bin/env python3
"""
Debug script to test JWT token verification
"""
import jwt
import os
import sys

# JWT settings
JWT_SECRET = os.getenv('JWT_SECRET', 'JWT_SECRET_KEY')
JWT_ALGORITHM = 'HS256'

def test_token(token_string):
    """Test JWT token verification"""
    try:
        print(f"Testing token: {token_string[:50]}...")
        print(f"Using secret: {JWT_SECRET}")
        print(f"Using algorithm: {JWT_ALGORITHM}")
        
        # Decode the token
        payload = jwt.decode(
            token_string,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )
        
        print("✅ Token is valid!")
        print("Payload:", payload)
        return True
        
    except jwt.ExpiredSignatureError:
        print("❌ Token has expired")
        return False
    except jwt.InvalidSignatureError:
        print("❌ Invalid signature - JWT secret mismatch")
        return False
    except jwt.InvalidTokenError as e:
        print(f"❌ Invalid token: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        token = sys.argv[1]
        test_token(token)
    else:
        print("Usage: python debug_token.py <jwt_token>")
        print("Or enter token when prompted:")
        token = input("Enter JWT token: ").strip()
        if token:
            test_token(token) 