from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import MONGO_DETAILS

DB_NAME = "data_web_db"

class DataBase:
    client: AsyncIOMotorClient = None
    database: AsyncIOMotorDatabase = None

db = DataBase()

def get_database() -> AsyncIOMotorDatabase:
    """
    Returns the database instance. This is not async anymore.
    """
    return db.database

async def connect_to_mongo():
    """
    Connects to the MongoDB and gets the database instance.
    """
    print("Connecting to MongoDB...")
    db.client = AsyncIOMotorClient(MONGO_DETAILS)
    db.database = db.client[DB_NAME]
    print(f"Successfully connected to MongoDB, using database '{DB_NAME}'.")

async def close_mongo_connection():
    """
    Closes the MongoDB connection.
    """
    print("Closing MongoDB connection...")
    db.client.close()
    print("Successfully closed MongoDB connection.")