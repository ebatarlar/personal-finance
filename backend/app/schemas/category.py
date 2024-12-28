from pydantic import BaseModel
from enum import Enum

class CategoryType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"

class CategoryCreate(BaseModel):
    type: CategoryType
    name: str

class CategoryResponse(BaseModel):
    type: CategoryType
    name: str
    is_default: bool = False
