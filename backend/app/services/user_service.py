from typing import Optional
from uuid import UUID
from app.core.database import db
from app.models.user import UserCreate, UserInDB, UserResponse, OAuthInfo
from app.core.security import get_password_hash, verify_password
from datetime import datetime, timezone
from bson import ObjectId
from fastapi import HTTPException

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
        current_time = datetime.now(timezone.utc)
        user_data = user.model_dump()
        
        # Handle password if provided
        if user.password:
            user_data["hashed_password"] = get_password_hash(user.password)
        del user_data["password"]  # Remove plain password
            
        user_in_db = UserInDB(
            **user_data,
            created_at=current_time,
            updated_at=current_time
        )
        
        # Convert UUID to string for MongoDB storage
        user_dict = user_in_db.model_dump()
        user_dict["id"] = str(user_dict["id"])
        
        # Insert into database
        await self.collection.insert_one(user_dict)
        return user_in_db
    
    async def authenticate_user(self, email: str, password: str) -> Optional[UserInDB]:
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not user.hashed_password:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    async def get_user_by_oauth(self, oauth_info: OAuthInfo) -> Optional[UserInDB]:
        if self.collection is None:
            raise Exception("Database not initialized")
            
        user_dict = await self.collection.find_one({
            "oauth_info.provider": oauth_info.provider,
            "oauth_info.provider_user_id": oauth_info.provider_user_id
        })
        
        if user_dict:
            if "_id" in user_dict:
                user_dict["_id"] = str(user_dict["_id"])
            return UserInDB(**user_dict)
        return None
    
    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        if self.collection is None:
            raise Exception("Database not initialized")
            
        user_dict = await self.collection.find_one({"email": email})
        if user_dict:
            # Convert MongoDB _id to string and remove it
            if "_id" in user_dict:
                user_dict["_id"] = str(user_dict["_id"])
            return UserInDB(**user_dict)
        return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[UserInDB]:
        """
        Get a user by their ID.
        
        Args:
            user_id (str): The ID of the user to retrieve
            
        Returns:
            Optional[UserInDB]: The user if found, None otherwise
        """
        if self.collection is None:
            raise Exception("Database not initialized")
            
        user_data = await self.collection.find_one({"id": user_id})
        if user_data is None:
            return None
            
        return UserInDB(**user_data)
    
    async def update_user(self, user_id: UUID, update_data: dict) -> Optional[UserInDB]:
        if self.collection is None:
            raise Exception("Database not initialized")
            
        current_time = datetime.now(timezone.utc)
        update_data["updated_at"] = current_time
        result = await self.collection.update_one(
            {"id": str(user_id)},
            {"$set": update_data}
        )
        if result.modified_count:
            return await self.get_user_by_id(user_id)
        return None

# Create a global instance
user_service = UserService()
