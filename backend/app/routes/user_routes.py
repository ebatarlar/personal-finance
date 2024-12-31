from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.user import UserCreate, UserResponse, OAuthInfo
from app.services.user_service import user_service
from app.core.security import Token, verify_token, create_tokens, verify_password
from pydantic import BaseModel

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

class LoginRequest(BaseModel):
    email: str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception
        
    user = await user_service.get_user_by_id(token_data.user_id)
    if user is None:
        raise credentials_exception
    return user

@router.post("/users/create", response_model=UserResponse)
async def create_user(user: UserCreate):
    """
    Create a new user account.
    
    Args:
        user (UserCreate): The user data to create, including:
            - email: User's email address
            - password: User's password
            - name: User's full name
    
    Returns:
        UserResponse: The created user's data (excluding sensitive information)
        
    Raises:
        HTTPException (500): If there's an error creating the user
    """
    try:
        created_user = await user_service.create_user(user)
        return UserResponse(**created_user.model_dump())
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating user: {str(e)}"
        )

@router.post("/users/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate a user and log them in.
    
    Args:
        form_data (OAuth2PasswordRequestForm): The login credentials from OAuth2 form
    
    Returns:
        Token: Access and refresh tokens for the authenticated user
        
    Raises:
        HTTPException (401): If authentication fails
        HTTPException (500): If there's an error during login
    """
    try:
        user = await user_service.get_user_by_email(form_data.username)  # OAuth2 form uses username field for email
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return create_tokens(str(user.id))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during login: {str(e)}"
        )

@router.post("/users/oauth", response_model=Token)
async def oauth_login(oauth_info: OAuthInfo, user_data: UserCreate):
    """
    Handle OAuth login/signup flow.
    
    Args:
        oauth_info (OAuthInfo): OAuth provider information
        user_data (UserCreate): User data from OAuth provider
    
    Returns:
        Token: Access and refresh tokens for the authenticated user
        
    Raises:
        HTTPException (500): If there's an error during OAuth login
    """
    try:
        # First, try to find existing user by OAuth info
        user = await user_service.get_user_by_oauth(oauth_info)
        if not user:
            # If not found, create new user with OAuth info
            user_data.oauth_info = oauth_info
            user = await user_service.create_user(user_data)
            
        # Generate tokens
        return create_tokens(str(user.id))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during OAuth login: {str(e)}"
        )

@router.get("/users/email/{email}", response_model=UserResponse)
async def get_user_by_email(email: str):
    """
    Get user information by email address.
    
    Args:
        email (str): The email address to look up
        
    Returns:
        UserResponse: The user's data if found
        
    Raises:
        HTTPException (404): If user is not found
        HTTPException (500): If there's an error fetching the user
    """
    try:
        user = await user_service.get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"User with email {email} not found"
            )
        return UserResponse(**user.model_dump())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching user: {str(e)}"
        )

@router.post("/token/refresh", response_model=Token)
async def refresh_token(refresh_request: RefreshRequest):
    """
    Get a new access token using a refresh token.
    
    Args:
        refresh_request (RefreshRequest): The refresh token
    
    Returns:
        Token: New access and refresh tokens
        
    Raises:
        HTTPException (401): If the refresh token is invalid
    """
    token_data = verify_token(refresh_request.refresh_token)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return create_tokens(token_data.user_id)
