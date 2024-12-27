from fastapi import APIRouter, HTTPException
from app.models.user import UserCreate, UserResponse
from app.services.user_service import user_service

router = APIRouter()

@router.post("/users/create", response_model=UserResponse)
async def create_user(user: UserCreate):
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
