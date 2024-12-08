from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    name: str
    github_id: Optional[str] = None
    
class UserCreate(UserBase):
    pass

class UserInDB(UserBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            UUID: str
        }
        
class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
