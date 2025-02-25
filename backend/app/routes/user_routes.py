from fastapi import APIRouter, HTTPException, Depends, status
from app.models.user import UserCreate, UserResponse
from app.services.user_service import user_service
from app.core.security import verify_token, oauth2_scheme

router = APIRouter()

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

@router.get("/users/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    """Get current user's information."""
    return current_user

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Get user by ID."""
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse(**user.model_dump())
