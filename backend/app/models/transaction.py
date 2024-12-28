import string
from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from enum import Enum



class Transaction(BaseModel):
    """Model representing a financial transaction."""
    """Represents a financial transaction with its attributes."""
    """Attributes:
        user_id (UUID): The unique identifier for the user.
        type (str): The type of transaction (expense or income).
        categories (List[str]): A list of categories associated with the transaction.
        amount (float): The amount of money involved in the transaction.
        date (datetime): The date of the transaction in Y-m-d format.
        description (Optional[str]): A brief description of the transaction.
        created_at (datetime): The timestamp when the transaction was created.
        updated_at (datetime): The timestamp when the transaction was last updated.
    """
    user_id: UUID
    type: str
    categories: List[str]  
    amount: float
    date: datetime  # Should be in Y-m-d format
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


    @field_validator('type')
    @classmethod
    def validate_type(cls, v: str) -> str:
        v = v.lower()
        if v not in ["income", "expense"]:
            raise ValueError("Transaction type must be either 'income' or 'expense'")
        return v

    @field_validator('date', mode='before')
    @classmethod
    def validate_date(cls, v):
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v)
            except ValueError:
                raise ValueError(f'Invalid date format: {v}. Use ISO format (YYYY-MM-DDTHH:MM:SS+HH:MM)')
        return v

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d') if hasattr(v, 'strftime') else v,
            UUID: lambda v: str(v)
        }