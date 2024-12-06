from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import db
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Personal Finance API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TransactionCreate(BaseModel):
    amount: float
    description: str
    date: datetime = datetime.now()

@app.on_event("startup")
async def startup():
    await db.connect_to_database(app)

@app.on_event("shutdown")
async def shutdown():
    await db.close_database_connection()

@app.get("/")
async def root():
    return {"message": "Welcome to Personal Finance API"}

@app.get("/test-db")
async def test_db():
    try:
        # Try to ping the database
        await db.client.admin.command('ping')
        return {"status": "success", "message": "Successfully connected to MongoDB!"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to connect to MongoDB: {str(e)}"}

@app.post("/api/transactions")
async def create_transaction(transaction: TransactionCreate):
    try:
        # Convert the transaction model to a dictionary
        transaction_dict = transaction.dict()
        
        # Insert the transaction into MongoDB
        result = await db.db.transactions.insert_one(transaction_dict)
        
        # Return the created transaction ID
        return {
            "id": str(result.inserted_id),
            "message": "Transaction created successfully"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
