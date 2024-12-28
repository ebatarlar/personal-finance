from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/default", response_model=List[CategoryResponse])
async def get_default_categories():
    return await CategoryService.get_default_categories()

@router.get("/custom/{user_id}", response_model=List[CategoryResponse])
async def get_custom_categories(user_id: str):
    return await CategoryService.get_user_custom_categories(user_id)

@router.get("/{user_id}", response_model=List[CategoryResponse])
async def get_all_categories(user_id: str):
    return await CategoryService.get_all_categories(user_id)

@router.post("/custom/{user_id}", response_model=CategoryResponse)
async def create_custom_category(user_id: str, category: CategoryCreate):
    return await CategoryService.add_custom_category(user_id, category)

@router.delete("/custom/{user_id}/{category_name}")
async def delete_custom_category(user_id: str, category_name: str):
    deleted = await CategoryService.delete_custom_category(user_id, category_name)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}
