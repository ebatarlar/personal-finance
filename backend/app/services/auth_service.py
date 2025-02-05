from datetime import datetime, timedelta
from typing import Optional, Union
from uuid import UUID
from fastapi import HTTPException, status, Depends
from app.core.security import verify_password, get_password_hash, create_tokens, verify_token
from app.models.user import UserCreate, UserInDB, OAuthInfo, UserExistResponse
from app.services.user_service import user_service
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import db, get_database
import logging
from pydantic import BaseModel

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.db = database
        self._token_blacklist = set()  # In-memory token blacklist. Consider using Redis in production
        
    async def register(self, user: UserCreate) -> Union[UserExistResponse, UserInDB]:
        """
        Register a new user.
        Returns UserExistResponse if user exists, otherwise returns the created UserInDB object.
        """
        try:
            logger.info(f"Starting registration process for email: {user.email}")
            
            # Validate input
            if not user.email:
                logger.error("Email is required")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email is required"
                )
                
            if not user.name or not user.surname:
                logger.error("Name and surname are required")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Name and surname are required"
                )
                
            # Check if user exists
            existing_user = await user_service.get_user_by_email(user.email)
            if existing_user:
                logger.info(f"User already exists: {user.email}")
                return UserExistResponse()
                
            # Rest of the registration logic remains the same...
            user_dict = user.model_dump()
            
            if user.password:
                if len(user.password) < 8:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Password must be at least 8 characters long"
                    )
                hashed_password = get_password_hash(user.password)
                del user_dict["password"]
                user_dict["hashed_password"] = hashed_password
            elif not user.oauth_info:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Either password or OAuth info must be provided"
                )
                
            created_user = await user_service.create_user(UserCreate(**user_dict))
            logger.info(f"Successfully created user: {user.email}")
            return created_user
            
        except HTTPException as he:
            logger.error(f"HTTP error during registration: {he.detail}")
            raise he
        except Exception as e:
            logger.error(f"Unexpected error during registration: {str(e)}")
            logger.exception(e)  # This will log the full stack trace
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error during registration: {str(e)}"
            )
    
    async def login(self, email: str, password: str) -> dict:
        """Authenticate user and return tokens."""
        user = await user_service.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        return create_tokens(str(user.id))
    
    async def oauth_login(self, oauth_info: OAuthInfo, user_data: UserCreate) -> dict:
        """Handle OAuth login/signup flow."""
        # First, check if user exists with OAuth provider
        existing_user = await user_service.get_user_by_oauth(
            oauth_info.provider,
            oauth_info.provider_user_id
        )
        
        if existing_user:
            return create_tokens(str(existing_user.id))
            
        # If not found by OAuth, check if user exists by email
        existing_user = await user_service.get_user_by_email(user_data.email)
        if existing_user:
            # Update existing user with OAuth info
            updated_user = await user_service.update_user_oauth(
                str(existing_user.id),
                oauth_info
            )
            if not updated_user:
                logger.error("Failed to update user with OAuth info")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update user with OAuth info"
                )
            return create_tokens(str(updated_user.id))
            
        # Create new user with OAuth info if no existing user found
        user_data.oauth_info = oauth_info
        new_user = await self.register(user_data)
        return create_tokens(str(new_user.id))
    
    async def logout(self, token: str) -> bool:
        """Logout user by blacklisting their token."""
        self._token_blacklist.add(token)
        return True
        
    async def refresh_token(self, refresh_token: str) -> dict:
        """Get new access token using refresh token."""
        # Verify the refresh token
        token_data = verify_token(refresh_token, is_refresh_token=True)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Check if token is blacklisted
        if refresh_token in self._token_blacklist:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        user = await user_service.get_user_by_id(token_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Create new tokens
        return create_tokens(str(user.id))

    async def send_verification_email(self, user_id: UUID) -> bool:
        """Send email verification link."""
        user = await user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        # TODO: Implement email sending logic
        # For now, just print the verification link
        tokens = create_tokens(str(user.id))
        verification_token = tokens["access_token"]
        print(f"Verification link: /auth/verify-email?token={verification_token}")
        return True
        
    async def verify_email(self, token: str) -> bool:
        """Verify user's email address."""
        token_data = verify_token(token)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid verification token"
            )
            
        # TODO: Update user's email verification status
        return True
        
    async def send_password_reset_email(self, email: str) -> bool:
        """Send password reset email."""
        user = await user_service.get_user_by_email(email)
        if not user:
            # Don't reveal if email exists
            return True
            
        # TODO: Implement email sending logic
        # For now, just print the reset link
        tokens = create_tokens(str(user.id))
        reset_token = tokens["access_token"]
        print(f"Password reset link: /auth/reset-password?token={reset_token}")
        return True
        
    async def reset_password(self, token: str, new_password: str) -> bool:
        """Reset user's password."""
        token_data = verify_token(token)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid reset token"
            )
            
        user = await user_service.get_user_by_id(token_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        # Update password
        hashed_password = get_password_hash(new_password)
        await self.db["users"].update_one(
            {"_id": user.id},
            {"$set": {"hashed_password": hashed_password}}
        )
        
        return True

# Create auth service factory
def get_auth_service():
    return AuthService(db)

# Use this in routes instead of a global instance
async def get_auth_service_dependency():
    if db.db is None:
        await db.connect_to_database(None)
    return AuthService(db.db)
