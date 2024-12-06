import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import certifi

async def test_connection():
    try:
        # Load environment variables
        load_dotenv()
        
        # Get MongoDB URL from environment
        MONGODB_URL = os.getenv("MONGODB_URL")
        
        if not MONGODB_URL:
            print("Error: MONGODB_URL not found in environment variables")
            return
            
        print("Attempting to connect to MongoDB...")
        
        # Create async client with SSL certificate verification
        client = AsyncIOMotorClient(
            MONGODB_URL,
            tlsCAFile=certifi.where()
        )
        
        # Test connection with ping
        await client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        
        # List databases
        databases = await client.list_database_names()
        print("Available databases:", databases)
        
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    asyncio.run(test_connection())
