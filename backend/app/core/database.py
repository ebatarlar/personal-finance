from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from fastapi import FastAPI
import os
from dotenv import load_dotenv
import certifi

load_dotenv()

class Database:
    client: Optional[AsyncIOMotorClient] = None
    db = None
    
    async def connect_to_database(self, app: FastAPI):
        try:
            MONGODB_URL = os.getenv("MONGODB_URL", "your_mongodb_connection_string_here")
            self.client = AsyncIOMotorClient(
                MONGODB_URL,
                tlsCAFile=certifi.where()
            )
            
            # Use the personal_finance database
            self.db = self.client.personal_finance
            
            # Verify connection
            await self.client.admin.command('ping')
            print("Successfully connected to MongoDB!")
            
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise e

    async def close_database_connection(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")

# Create a database instance
db = Database()
