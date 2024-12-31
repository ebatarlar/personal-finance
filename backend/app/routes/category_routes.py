from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.category_service import category_service
from app.routes.user_routes import get_current_user
from app.models.user import UserInDB

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/default", response_model=List[CategoryResponse])
async def get_default_categories():
    """
    Get a list of default expense categories.
    
    Returns:
        List[CategoryResponse]: A list of default categories available to all users
        
    Raises:
        HTTPException (500): If there's an error fetching the categories
    """
    try:
        return await category_service.get_default_categories()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching default categories: {str(e)}"
        )

@router.get("/custom/{user_id}", response_model=List[CategoryResponse])
async def get_custom_categories(user_id: str, current_user: UserInDB = Depends(get_current_user)):
    """
    Get all custom categories created by a specific user.
    
    Args:
        user_id (str): The ID of the user whose custom categories to retrieve
        current_user (UserInDB): The authenticated user (injected by FastAPI)
        
    Returns:
        List[CategoryResponse]: A list of custom categories created by the user
        
    Raises:
        HTTPException (401): If user is not authenticated
        HTTPException (403): If user tries to access another user's categories
        HTTPException (500): If there's an error fetching the categories
    """
    if user_id != str(current_user.id):
        raise HTTPException(
            status_code=403,
            detail="Cannot access another user's categories"
        )
        
    try:
        return await category_service.get_user_custom_categories(user_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching custom categories: {str(e)}"
        )

@router.get("/{user_id}", response_model=List[CategoryResponse])
async def get_all_categories(user_id: str, current_user: UserInDB = Depends(get_current_user)):
    """
    Get all categories (both default and custom) available to a user.
    
    Args:
        user_id (str): The ID of the user
        current_user (UserInDB): The authenticated user (injected by FastAPI)
        
    Returns:
        List[CategoryResponse]: A list of all categories available to the user
        
    Raises:
        HTTPException (401): If user is not authenticated
        HTTPException (403): If user tries to access another user's categories
        HTTPException (500): If there's an error fetching the categories
    """
    if user_id != str(current_user.id):
        raise HTTPException(
            status_code=403,
            detail="Cannot access another user's categories"
        )
        
    try:
        return await category_service.get_all_categories(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching categories: {str(e)}"
        )

@router.post("/custom/{user_id}", response_model=CategoryResponse)
async def create_custom_category(
    user_id: str, 
    category: CategoryCreate,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Create a new custom category for a specific user.
    
    Args:
        user_id (str): The ID of the user creating the category
        category (CategoryCreate): The category data to create
        current_user (UserInDB): The authenticated user (injected by FastAPI)
        
    Returns:
        CategoryResponse: The created category
        
    Raises:
        HTTPException (401): If user is not authenticated
        HTTPException (403): If user tries to create a category for another user
        HTTPException (500): If there's an error creating the category
    """
    if user_id != str(current_user.id):
        raise HTTPException(
            status_code=403,
            detail="Cannot create categories for another user"
        )
        
    try:
        return await category_service.create_custom_category(user_id, category)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating custom category: {str(e)}"
        )

@router.delete("/custom/{user_id}/{category_name}")
async def delete_custom_category(
    user_id: str, 
    category_name: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Delete a custom category for a specific user.
    
    Args:
        user_id (str): The ID of the user
        category_name (str): The name of the category to delete
        current_user (UserInDB): The authenticated user (injected by FastAPI)
        
    Returns:
        dict: A message confirming successful deletion
        
    Raises:
        HTTPException (401): If user is not authenticated
        HTTPException (403): If user tries to delete another user's category
        HTTPException (500): If there's an error deleting the category
    """
    if user_id != str(current_user.id):
        raise HTTPException(
            status_code=403,
            detail="Cannot delete another user's categories"
        )
        
    try:
        await category_service.delete_custom_category(user_id, category_name)
        return {"message": f"Category '{category_name}' deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting custom category: {str(e)}"
        )
