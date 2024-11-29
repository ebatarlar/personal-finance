from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import os
from dotenv import load_dotenv
import logging
import certifi

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class MongoDBConnection:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._client:
            self.connect()

    def connect(self):
        """Establish connection to MongoDB"""
        try:
            # Get MongoDB URI from environment variable
            mongodb_uri = os.getenv('MONGODB_URI')
            if not mongodb_uri:
                raise ValueError("MongoDB URI not found in environment variables")

            # Create MongoDB client with SSL certificate verification
            self._client = MongoClient(mongodb_uri, tlsCAFile=certifi.where())
            
            # Verify connection
            self._client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
            
            # Get database
            self.db = self._client[os.getenv('MONGODB_DB_NAME', 'personal_finance')]
            
        except ConnectionFailure as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            raise
        except OperationFailure as e:
            logger.error(f"Authentication failed: {e}")
            raise
        except Exception as e:
            logger.error(f"An error occurred while connecting to MongoDB: {e}")
            raise

    def get_database(self):
        """Get database instance"""
        return self.db

    def close_connection(self):
        """Close MongoDB connection"""
        if self._client:
            self._client.close()
            self._client = None
            logger.info("MongoDB connection closed")

# Example usage
def get_db_connection():
    """Get MongoDB connection instance"""
    return MongoDBConnection().get_database()

# Example of how to use the connection
if __name__ == "__main__":
    try:
        # Get database connection
        db = get_db_connection()
        
        # Example: Create a test document
        result = db.test_collection.insert_one({"test": "Hello MongoDB!"})
        logger.info(f"Inserted document with ID: {result.inserted_id}")
        
        # Example: Retrieve the document
        doc = db.test_collection.find_one({"test": "Hello MongoDB!"})
        logger.info(f"Retrieved document: {doc}")
        
    except Exception as e:
        logger.error(f"Error during database operations: {e}")
    finally:
        # Close connection
        MongoDBConnection().close_connection()
