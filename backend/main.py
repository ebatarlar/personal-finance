from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import db
from pydantic import BaseModel
from datetime import datetime
from app.routes.user_routes import router as user_router
from app.routes.transaction_routes import router as transaction_router
from app.routes.category_routes import router as category_router
from app.routes.auth_routes import router as auth_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.connect_to_database(app)
    yield
    # Shutdown
    await db.close_database_connection()

app = FastAPI(title="Personal Finance API", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://frontend-iota-ruby.vercel.app"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include auth routes
app.include_router(auth_router, prefix="/api", tags=["auth"])

# Include user routes
app.include_router(user_router, prefix="/api", tags=["users"])

# Include transaction routes
app.include_router(transaction_router, prefix="/api", tags=["transactions"])

# Include category routes
app.include_router(category_router, prefix="/api", tags=["categories"])


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
