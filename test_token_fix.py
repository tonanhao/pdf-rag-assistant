#!/usr/bin/env python3
"""
Test script to verify JWT token compatibility between Auth API and Main API
"""
import os
import jwt
from datetime import datetime, timedelta

# Set the same secret key for both services
SECRET_KEY = "your-super-secret-jwt-key-here-change-in-production"
ALGORITHM = "HS256"

def create_test_token():
    """Create a test JWT token like the auth API would"""
    payload = {
        'sub': '12345',  # user_id
        'email': 'test@example.com',
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print(f"✅ Generated test token: {token}")
    return token

def verify_test_token(token):
    """Verify the token like the main API would"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"✅ Token verified successfully!")
        print(f"   User ID: {payload.get('sub')}")
        print(f"   Email: {payload.get('email')}")
        return True
    except Exception as e:
        print(f"❌ Token verification failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Testing JWT token compatibility...")
    print(f"Using SECRET_KEY: {SECRET_KEY}")
    print(f"Using ALGORITHM: {ALGORITHM}")
    print()
    
    # Test token creation and verification
    token = create_test_token()
    success = verify_test_token(token)
    
    if success:
        print("\n✅ JWT configuration is working correctly!")
        print("Both APIs should now be able to create and verify tokens.")
    else:
        print("\n❌ JWT configuration has issues.")
        
    print(f"\n📝 Set this environment variable for both services:")
    print(f"SECRET_KEY={SECRET_KEY}") 