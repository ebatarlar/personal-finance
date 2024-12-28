from typing import List
from app.schemas.category import CategoryCreate, CategoryResponse
from app.core.database import db
from fastapi import HTTPException

class CategoryService:
    def __init__(self):
        self.db = db
    
    @property
    def collection(self):
        if self.db is None or self.db.db is None:
            return None
        return self.db.db.users

    async def get_default_categories(self) -> List[CategoryResponse]:
        if self.db is None or self.db.db is None:
            raise Exception("Database not initialized")
            
        cursor = self.db.db.defaultCategories.find({})
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

    async def get_user_custom_categories(self, user_id: str) -> List[CategoryResponse]:
        if self.collection is None:
            raise Exception("Database not initialized")
            
        user = await self.collection.find_one({"id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return [CategoryResponse(
            type=category["type"],
            name=category["name"],
            is_default=False
        ) for category in user.get("customCategories", [])]

    async def get_all_categories(self, user_id: str) -> List[CategoryResponse]:
        default_categories = await self.get_default_categories()
        custom_categories = await self.get_user_custom_categories(user_id)
        return default_categories + custom_categories

    async def add_custom_category(self, user_id: str, category: CategoryCreate) -> CategoryResponse:
        if self.collection is None:
            raise Exception("Database not initialized")
            
        new_category = {
            "type": category.type,
            "name": category.name
        }
        
        result = await self.collection.update_one(
            {"id": user_id},
            {"$push": {"customCategories": new_category}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
            
        return CategoryResponse(**new_category, is_default=False)

    async def delete_custom_category(self, user_id: str, category_name: str) -> bool:
        if self.collection is None:
            raise Exception("Database not initialized")
            
        result = await self.collection.update_one(
            {"id": user_id},
            {"$pull": {"customCategories": {"name": category_name}}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Category not found or user not found")
            
        return True

# Create a global instance
category_service = CategoryService()
