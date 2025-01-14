from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Argon2 with recommended parameters
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__time_cost=2,        # Number of iterations
    argon2__memory_cost=102400,  # Memory usage in kibibytes (100 MB)
    argon2__parallelism=8       # Number of parallel threads
)

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "development_secret_key_123")  # Make sure to set this in .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# OAuth2 scheme for token handling
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: str

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    """Create access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Create refresh token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, is_refresh_token: bool = False) -> Optional[TokenData]:
    """Verify JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
            
        # For refresh tokens, verify the token type
        if is_refresh_token and payload.get("token_type") != "refresh":
            return None
            
        return TokenData(user_id=user_id)
    except JWTError:
        return None

def create_tokens(user_id: str) -> dict:
    """Create access and refresh tokens."""
    access_token_data = {"sub": user_id, "token_type": "access"}
    refresh_token_data = {"sub": user_id, "token_type": "refresh"}
    
    return {
        "access_token": create_access_token(access_token_data),
        "refresh_token": create_refresh_token(refresh_token_data),
        "token_type": "bearer"
    }
