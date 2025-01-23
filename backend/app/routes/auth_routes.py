from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from typing import Union
from app.models.user import UserCreate, UserResponse, OAuthInfo, UserExistResponse
from app.services.auth_service import AuthService, get_auth_service_dependency
from app.core.security import Token
from app.core.rate_limit import aggressive_limiter, normal_limiter, relaxed_limiter
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Request/Response Models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class MessageResponse(BaseModel):
    message: str

@router.post("/register", response_model=Union[UserResponse, UserExistResponse])
@aggressive_limiter
async def register(
    request: Request,
    user: UserCreate,
    auth_service: AuthService = Depends(get_auth_service_dependency)
):
    """Register a new user."""
    try:
        logger.info(f"Attempting to register user with email: {user.email}")
        if not user.password and not user.oauth_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either password or OAuth info must be provided"
            )
        return await auth_service.register(user)
    except HTTPException as he:
        logger.error(f"HTTP error during registration: {he.detail}")
        raise he
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during registration: {str(e)}"
        )

@router.post("/login", response_model=TokenResponse)
@aggressive_limiter
async def login(
    request: Request,
    credentials: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service_dependency)
):
    """Authenticate user and return tokens."""
    try:
        tokens = await auth_service.login(credentials.email, credentials.password)
        return TokenResponse(**tokens)
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.post("/oauth", response_model=TokenResponse)
@normal_limiter
async def oauth_login(
    request: Request,
    oauth_info: OAuthInfo,
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service_dependency)
):
    """Handle OAuth login/signup flow."""
    tokens = await auth_service.oauth_login(oauth_info, user_data)
    return TokenResponse(**tokens)

@router.post("/logout", response_model=MessageResponse)
@normal_limiter
async def logout(
    request: Request,
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service_dependency)
):
    """Logout user and invalidate token."""
    await auth_service.logout(token)
    return {"message": "Successfully logged out"}

@router.post("/refresh-token", response_model=TokenResponse)
@relaxed_limiter
async def refresh_token(
    request: Request,
    refresh_request: RefreshRequest,
    auth_service: AuthService = Depends(get_auth_service_dependency)
):
    """Get new access token using refresh token."""
    tokens = await auth_service.refresh_token(refresh_request.refresh_token)
    return TokenResponse(**tokens)

@router.post("/verify-email", response_model=MessageResponse)
@normal_limiter
async def verify_email(
    request: Request,
    token: str,
    auth_service: AuthService = Depends(get_auth_service_dependency)
):
    """Verify user's email address."""
    await auth_service.verify_email(token)
    return {"message": "Email successfully verified"}

@router.post("/send-verification-email", response_model=MessageResponse)
@normal_limiter
async def send_verification_email(
    request: Request,
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service_dependency)
):
    """Send email verification link."""
    await auth_service.send_verification_email(token)
    return {"message": "Verification email sent"}

@router.post("/forgot-password", response_model=MessageResponse)
@aggressive_limiter
async def forgot_password(
    request: Request,
    request_data: PasswordResetRequest,
    auth_service: AuthService = Depends(get_auth_service_dependency)
):
    """Send password reset email."""
    await auth_service.send_password_reset_email(request_data.email)
    return {"message": "If your email is registered, you will receive a password reset link"}

@router.post("/reset-password", response_model=MessageResponse)
@aggressive_limiter
async def reset_password(
    request: Request,
    reset_data: PasswordResetConfirm,
    auth_service: AuthService = Depends(get_auth_service_dependency)
):
    """Reset user's password."""
    await auth_service.reset_password(reset_data.token, reset_data.new_password)
    return {"message": "Password successfully reset"}
