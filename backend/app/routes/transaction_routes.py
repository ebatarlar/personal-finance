from fastapi import APIRouter, HTTPException, Depends
from app.models.transaction import Transaction
from app.services.transaction_service import transaction_service
from app.routes.user_routes import get_current_user
from app.models.user import UserInDB
import traceback
from uuid import UUID
from fastapi import Response

router = APIRouter()


@router.post("/transactions/create")
async def create_transaction(transaction: Transaction, current_user: UserInDB = Depends(get_current_user)):
    """
    Create a new financial transaction.
    
    Args:
        transaction (Transaction): The transaction data to create, including:
            - amount: Decimal amount of the transaction
            - category: Category of the transaction
            - description: Optional description
            - date: Date of the transaction
        current_user (UserInDB): The authenticated user (injected by FastAPI)
    
    Returns:
        dict: A message confirming successful creation and the transaction ID
        
    Raises:
        HTTPException (401): If user is not authenticated
        HTTPException (500): If there's an error creating the transaction
    """
    try:
        # Ensure the transaction belongs to the authenticated user
        transaction.user_id = current_user.id
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
async def get_user_transactions(user_id: UUID, current_user: UserInDB = Depends(get_current_user)):
    """
    Get all transactions for a specific user.
    
    Args:
        user_id (UUID): The ID of the user whose transactions to retrieve
        current_user (UserInDB): The authenticated user (injected by FastAPI)
        
    Returns:
        List[Transaction]: List of transactions
        
    Raises:
        HTTPException (401): If user is not authenticated
        HTTPException (403): If user tries to access another user's transactions
        HTTPException (500): If there's an error fetching the transactions
    """
    # Ensure users can only access their own transactions
    if str(user_id) != str(current_user.id):
        raise HTTPException(
            status_code=403,
            detail="Cannot access another user's transactions"
        )
        
    try:
        return await transaction_service.get_user_transactions(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching transactions: {str(e)}"
        )