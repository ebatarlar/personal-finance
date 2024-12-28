from typing import List
from app.schemas.category import CategoryCreate, CategoryResponse
from app.core.database import db
from fastapi import HTTPException

class CategoryService:
    @staticmethod
    async def get_default_categories() -> List[CategoryResponse]:
        cursor = db.db.defaultCategories.find({})
        categories = []
        async for category in cursor:
            categories.append(
                CategoryResponse(
                    type=category["type"],
                    name=category["name"],
                    is_default=True
                )
            )
        return categories

    @staticmethod
    async def get_user_custom_categories(user_id: str) -> List[CategoryResponse]:
        user = await db.db.users.find_one({"id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return [CategoryResponse(
            type=category["type"],
            name=category["name"],
            is_default=False
        ) for category in user.get("customCategories", [])]

    @staticmethod
    async def get_all_categories(user_id: str) -> List[CategoryResponse]:
        default_categories = await CategoryService.get_default_categories()
        custom_categories = await CategoryService.get_user_custom_categories(user_id)
        return default_categories + custom_categories

    @staticmethod
    async def add_custom_category(user_id: str, category: CategoryCreate) -> CategoryResponse:
        new_category = {
            "type": category.type,
            "name": category.name
        }
        
        result = await db.db.users.update_one(
            {"id": user_id},
            {"$push": {"customCategories": new_category}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
            
        return CategoryResponse(**new_category, is_default=False)

    @staticmethod
    async def delete_custom_category(user_id: str, category_name: str) -> bool:
        result = await db.db.users.update_one(
            {"id": user_id},
            {"$pull": {"customCategories": {"name": category_name}}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Category not found or user not found")
            
        return True
