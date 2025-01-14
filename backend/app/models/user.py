from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class OAuthProvider(str, Enum):
    GITHUB = "github"
    GOOGLE = "google"

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1)
    surname: str = Field(..., min_length=1)
    is_active: bool = True
    is_verified: bool = False
    
class OAuthInfo(BaseModel):
    provider: OAuthProvider
    provider_user_id: str

class UserCreate(UserBase):
    password: Optional[str] = Field(None, min_length=8)
    oauth_info: Optional[OAuthInfo] = None
    hashed_password: Optional[str] = None
    
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
        from_attributes = True
        json_encoders = {
            UUID: str,
            datetime: lambda dt: dt.isoformat()
        }
        
class UserExistResponse(BaseModel):
    status: str = "user_exist"
    

class UserResponse(UserBase):
    id: UUID
    oauth_info: Optional[OAuthInfo] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            UUID: str,
            datetime: lambda dt: dt.isoformat()
        }
