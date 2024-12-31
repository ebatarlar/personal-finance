from datetime import datetime , timezone
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class OAuthProvider(str, Enum):
    GITHUB = "github"
    GOOGLE = "google"

class UserBase(BaseModel):
    email: EmailStr
    name: str
    surname: str
    
class OAuthInfo(BaseModel):
    provider: OAuthProvider
    provider_user_id: str

class UserCreate(UserBase):
    password: Optional[str] = None
    oauth_info: Optional[OAuthInfo] = None
    
    @property
    def is_oauth_user(self) -> bool:
        return self.oauth_info is not None

class UserInDB(UserBase):
    id: UUID = Field(default_factory=uuid4)
    hashed_password: Optional[str] = None
    oauth_info: Optional[OAuthInfo] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        json_encoders = {
            UUID: str
        }
        
class UserResponse(UserBase):
    id: UUID
    oauth_info: Optional[OAuthInfo] = None
    created_at: datetime
    updated_at: datetime
