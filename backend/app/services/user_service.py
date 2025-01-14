from typing import Optional
from uuid import UUID
from app.core.database import db
from app.models.user import UserCreate, UserInDB, UserResponse, OAuthInfo
from app.core.security import get_password_hash, verify_password
from datetime import datetime, timezone
from bson import ObjectId
from fastapi import HTTPException
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserService:
    def __init__(self):
        self.db = db
        logger.info("UserService initialized")
    
    @property
    def collection(self):
        if self.db is None or self.db.db is None:
            logger.error("Database not initialized")
            return None
        return self.db.db.users
    
    async def create_user(self, user: UserCreate) -> UserInDB:
        """Create a new user in the database."""
        try:
            if self.collection is None:
                logger.error("Database not initialized")
                raise Exception("Database not initialized")
                
            # Check if user already exists
            logger.info(f"Checking if user exists: {user.email}")
            existing_user = await self.get_user_by_email(user.email)
            if existing_user:
                logger.info(f"User already exists: {user.email}")
                return existing_user
                
            # Create new user
            logger.info(f"Creating new user: {user.email}")
            current_time = datetime.now(timezone.utc)
            user_data = user.model_dump()
            logger.debug(f"User data before processing: {user_data}")
            
            # Create UserInDB instance
            logger.info("Creating UserInDB instance")
            
            # Remove password if it exists
            if "password" in user_data:
                del user_data["password"]
            
            # Create user instance
            user_in_db = UserInDB(
                **user_data,
                created_at=current_time,
                updated_at=current_time
            )
            
            # Convert to dict for MongoDB
            user_dict = user_in_db.model_dump()
            user_dict["id"] = str(user_dict["id"])
            logger.debug(f"User dict for MongoDB: {user_dict}")
            
            # Insert into database
            logger.info(f"Inserting user into database: {user.email}")
            result = await self.collection.insert_one(user_dict)
            logger.info(f"User inserted with ID: {result.inserted_id}")
            
            return user_in_db
            
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            logger.exception(e)
            raise
        
    async def authenticate_user(self, email: str, password: str) -> Optional[UserInDB]:
        """Authenticate a user with email and password."""
        try:
            logger.info(f"Attempting to authenticate user: {email}")
            user = await self.get_user_by_email(email)
            if not user:
                logger.info(f"User not found: {email}")
                return None
            if not user.hashed_password:
                logger.error(f"User has no password: {email}")
                return None
            if not verify_password(password, user.hashed_password):
                logger.info(f"Invalid password for user: {email}")
                return None
            logger.info(f"User authenticated successfully: {email}")
            return user
        except Exception as e:
            logger.error(f"Error authenticating user: {str(e)}")
            logger.exception(e)
            return None
    
    async def get_user_by_oauth(self, provider: str, provider_user_id: str) -> Optional[UserInDB]:
        """Get user by OAuth provider and provider user ID."""
        try:
            if self.collection is None:
                logger.error("Database not initialized")
                return None
            
            logger.info(f"Looking up user by OAuth: {provider}, {provider_user_id}")
            user_dict = await self.collection.find_one({
                "oauth_info.provider": provider,
                "oauth_info.provider_user_id": provider_user_id
            })
            
            if not user_dict:
                logger.info("No user found with these OAuth credentials")
                return None
                
            logger.info(f"Found user with OAuth credentials: {user_dict.get('email')}")
            return UserInDB(**user_dict)
            
        except Exception as e:
            logger.error(f"Error getting user by OAuth: {str(e)}")
            logger.exception(e)
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        try:
            if self.collection is None:
                logger.error("Database not initialized")
                raise Exception("Database not initialized")
                
            logger.info(f"Getting user by email: {email}")
            user_dict = await self.collection.find_one({"email": email})
            if user_dict:
                logger.info(f"User found by email: {email}")
                # Convert MongoDB _id to string and remove it
                if "_id" in user_dict:
                    user_dict["_id"] = str(user_dict["_id"])
                return UserInDB(**user_dict)
            logger.info(f"No user found by email: {email}")
            return None
        except Exception as e:
            logger.error(f"Error getting user by email: {str(e)}")
            logger.exception(e)
            return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[UserInDB]:
        """
        Get a user by their ID.
        
        Args:
            user_id (str): The ID of the user to retrieve
            
        Returns:
            Optional[UserInDB]: The user if found, None otherwise
        """
        try:
            if self.collection is None:
                logger.error("Database not initialized")
                raise Exception("Database not initialized")
                
            logger.info(f"Getting user by ID: {user_id}")
            user_data = await self.collection.find_one({"id": user_id})
            if user_data is None:
                logger.info(f"No user found by ID: {user_id}")
                return None
                
            logger.info(f"User found by ID: {user_id}")
            return UserInDB(**user_data)
        except Exception as e:
            logger.error(f"Error getting user by ID: {str(e)}")
            logger.exception(e)
            return None

    async def update_user(self, user_id: UUID, update_data: dict) -> Optional[UserInDB]:
        try:
            if self.collection is None:
                logger.error("Database not initialized")
                raise Exception("Database not initialized")
                
            logger.info(f"Updating user with ID: {user_id}")
            current_time = datetime.now(timezone.utc)
            update_data["updated_at"] = current_time
            result = await self.collection.update_one(
                {"id": str(user_id)},
                {"$set": update_data}
            )
            if result.modified_count:
                logger.info(f"User updated successfully with ID: {user_id}")
                return await self.get_user_by_id(user_id)
            logger.info(f"No user updated with ID: {user_id}")
            return None
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            logger.exception(e)
            return None

    async def update_user_oauth(self, user_id: str, oauth_info: OAuthInfo) -> Optional[UserInDB]:
        """Update user's OAuth information."""
        try:
            if self.collection is None:
                logger.error("Database not initialized")
                return None
            
            logger.info(f"Updating OAuth info for user {user_id}")
            
            # First get the user to ensure they exist
            existing_user = await self.collection.find_one({"id": user_id})
            if not existing_user:
                logger.error(f"No user found with ID {user_id}")
                return None

            # Update the user's OAuth info
            result = await self.collection.update_one(
                {"id": user_id},
                {"$set": {
                    "oauth_info": oauth_info.model_dump(),
                    "updated_at": datetime.now(timezone.utc)
                }}
            )
            
            if result.modified_count == 0:
                logger.error(f"Failed to update OAuth info for user {user_id}")
                return None
                
            # Get the updated user document
            updated_user_doc = await self.collection.find_one({"id": user_id})
            if not updated_user_doc:
                logger.error(f"Could not fetch updated user with ID {user_id}")
                return None
                
            logger.info(f"Successfully updated OAuth info for user {user_id}")
            # Convert MongoDB _id to string before creating UserInDB
            if "_id" in updated_user_doc:
                updated_user_doc["_id"] = str(updated_user_doc["_id"])
            return UserInDB(**updated_user_doc)
            
        except Exception as e:
            logger.error(f"Error updating user OAuth info: {str(e)}")
            logger.exception(e)
            return None

# Create a global instance
user_service = UserService()
