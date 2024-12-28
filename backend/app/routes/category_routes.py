from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.category_service import category_service

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/default", response_model=List[CategoryResponse])
async def get_default_categories():
    try:
        return await category_service.get_default_categories()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching default categories: {str(e)}"
        )

@router.get("/custom/{user_id}", response_model=List[CategoryResponse])
async def get_custom_categories(user_id: str):
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
async def get_all_categories(user_id: str):
    try:
        return await category_service.get_all_categories(user_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching categories: {str(e)}"
        )

@router.post("/custom/{user_id}", response_model=CategoryResponse)
async def create_custom_category(user_id: str, category: CategoryCreate):
    try:
        return await category_service.add_custom_category(user_id, category)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating custom category: {str(e)}"
        )

@router.delete("/custom/{user_id}/{category_name}")
async def delete_custom_category(user_id: str, category_name: str):
    try:
        deleted = await category_service.delete_custom_category(user_id, category_name)
        if deleted:
            return {"message": "Category deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting custom category: {str(e)}"
        )
