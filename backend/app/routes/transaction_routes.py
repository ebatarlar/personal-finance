from fastapi import APIRouter, HTTPException
from app.models.transaction import Transaction
from app.services.transaction_service import transaction_service
import traceback
from uuid import UUID
from fastapi import Response

router = APIRouter()


@router.post("/transactions/create")
async def create_transaction(transaction: Transaction):
    try:
        print(f"Received transaction data: {transaction.model_dump()}")  # Debug log
        result = await transaction_service.create_transaction(transaction)
        return {"message": "Transaction created successfully", "transaction_id": str(result.user_id)}
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error in create_transaction: {str(e)}\n{error_trace}")  # Debug log with traceback
        raise HTTPException(
            status_code=500,
            detail=f"Error creating transaction: {str(e)}"
        )
@router.get("/transactions/user/{user_id}")
async def get_user_transactions(user_id: UUID):
    try:
        transactions = await transaction_service.get_user_transactions(user_id)
        return {"transactions": transactions}
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error in get_user_transactions: {str(e)}\n{error_trace}")  # Debug log with traceback
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching transactions: {str(e)}"
        )