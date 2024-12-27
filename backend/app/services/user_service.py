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
        if self.db is None or self.db.db is None:
            return None
        return self.db.db.users
    
    async def create_user(self, user: UserCreate) -> UserInDB:
        if self.collection is None:
            raise Exception("Database not initialized")
            
        # Check if user already exists
        existing_user = await self.get_user_by_email(user.email)
        if existing_user:
            return existing_user
            
        # Create new user
        current_time = datetime.now(datetime.timezone.utc)  
        user_in_db = UserInDB(
            **user.model_dump(),
            created_at=current_time,
            updated_at=current_time
        )
        
        # Convert UUID to string for MongoDB storage
        user_dict = user_in_db.model_dump()
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
            
        current_time = datetime.now(datetime.timezone.utc)  # Updated to use timezone-aware UTC time
        update_data["updated_at"] = current_time
        result = await self.collection.update_one(
            {"id": str(user_id)},
            {"$set": update_data.model_dump()}
        )
        if result.modified_count:
            return await self.get_user_by_id(user_id)
        return None

# Create a global instance
user_service = UserService()
