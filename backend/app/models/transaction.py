from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from enum import Enum

class TransactionType(Enum):
    EXPENSE = 0
    INCOME = 1

class Transaction(BaseModel):
    """Model representing a financial transaction."""
    """Represents a financial transaction with its attributes."""
    """Attributes:
        user_id (UUID): The unique identifier for the user.
        type (TransactionType): The type of transaction (expense or income).
        categories (List[str]): A list of categories associated with the transaction.
        amount (float): The amount of money involved in the transaction.
        date (datetime): The date of the transaction in Y-m-d format.
        description (Optional[str]): A brief description of the transaction.
        created_at (datetime): The timestamp when the transaction was created.
        updated_at (datetime): The timestamp when the transaction was last updated.
    """
    user_id: UUID
    type: TransactionType
    categories: List[str]  
    amount: float
    date: datetime  # Should be in Y-m-d format
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator('type', mode='before')
    @classmethod
    def validate_type(cls, v):
        if isinstance(v, (int, str)):
            try:
                if isinstance(v, str):
                    return TransactionType[v.upper()]
                return TransactionType(v)
            except (KeyError, ValueError):
                raise ValueError(f'Invalid transaction type: {v}')
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
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v),
            TransactionType: lambda v: v.value
        }