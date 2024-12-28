from datetime import datetime
from uuid import UUID
from app.models.transaction import Transaction
from app.core.database import db

class TransactionService:
    def __init__(self):
        self.db = db

    @property
    def collection(self):
        return self.db.db.transactions if hasattr(self.db, 'db') and self.db.db is not None else None

    async def create_transaction(self, transaction: Transaction):
        if self.collection is None:
            raise Exception("Database not initialized")

        transaction_dict = transaction.model_dump()

        # Convert UUID to string for MongoDB storage
        transaction_dict["user_id"] = str(transaction_dict["user_id"])
        
        # Store type as string
        if transaction_dict["type"] not in ["income", "expense"]:
            raise ValueError("Transaction type must be either 'income' or 'expense'")
        
        # Convert datetime objects to ISO format strings
        for field in ["date", "created_at", "updated_at"]:
            if transaction_dict.get(field):
                transaction_dict[field] = transaction_dict[field].isoformat()

        try:
            # Insert into database
            result = await self.collection.insert_one(transaction_dict)
            if not result.inserted_id:
                raise Exception("Failed to insert transaction")
            return transaction
        except Exception as e:
            print(f"Error inserting transaction: {str(e)}")
            raise Exception(f"Database error: {str(e)}")
    async def get_user_transactions(self, user_id: UUID):
        if self.collection is None:
            raise Exception("Database not initialized")
            
        transactions = []
        async for transaction in self.collection.find({"user_id": str(user_id)}):
            # Convert MongoDB _id to string and remove it
            if "_id" in transaction:
                transaction["_id"] = str(transaction["_id"])
                del transaction["_id"]
            transactions.append(Transaction(**transaction))
        return transactions
# Create a global instance
transaction_service = TransactionService()