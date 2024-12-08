from typing import Optional
from uuid import UUID
from app.core.database import db
from app.models.user import UserCreate, UserInDB, UserResponse
from datetime import datetime
from bson import ObjectId

class UserService:
    def __init__(self):
        self.db = db
    
    @property
    def collection(self):
        return self.db.db.users if self.db.db is not None else None
    
    async def create_user(self, user: UserCreate) -> UserInDB:
        if self.collection is None:
            raise Exception("Database not initialized")
            
        # Check if user already exists
        existing_user = await self.get_user_by_email(user.email)
        if existing_user:
            return existing_user
            
        # Create new user
        user_in_db = UserInDB(
            **user.dict(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Convert UUID to string for MongoDB storage
        user_dict = user_in_db.dict()
        user_dict["id"] = str(user_dict["id"])
        
        # Insert into database
        await self.collection.insert_one(user_dict)
        return user_in_db
    
    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        if self.collection is None:
            raise Exception("Database not initialized")
            
        user_dict = await self.collection.find_one({"email": email})
        if user_dict:
            # Convert MongoDB _id to string and remove it
            if "_id" in user_dict:
                user_dict["_id"] = str(user_dict["_id"])
                del user_dict["_id"]
            return UserInDB(**user_dict)
        return None
    
    async def get_user_by_id(self, user_id: UUID) -> Optional[UserInDB]:
        if self.collection is None:
            raise Exception("Database not initialized")
            
        user_dict = await self.collection.find_one({"id": str(user_id)})
        if user_dict:
            # Convert MongoDB _id to string and remove it
            if "_id" in user_dict:
                user_dict["_id"] = str(user_dict["_id"])
                del user_dict["_id"]
            return UserInDB(**user_dict)
        return None
    
    async def update_user(self, user_id: UUID, update_data: dict) -> Optional[UserInDB]:
        if self.collection is None:
            raise Exception("Database not initialized")
            
        update_data["updated_at"] = datetime.utcnow()
        result = await self.collection.update_one(
            {"id": str(user_id)},
            {"$set": update_data}
        )
        if result.modified_count:
            return await self.get_user_by_id(user_id)
        return None

# Create a global instance
user_service = UserService()
