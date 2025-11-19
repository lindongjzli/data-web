from motor.motor_asyncio import AsyncIOMotorClient
from app.models.user_model import UserCreate, UserInDB
from app.services.security_service import get_password_hash
from app.db.mongodb_utils import get_database

# This would be your users collection
# In a real app, you might want to get this from a more central place
USER_COLLECTION = "users"

async def get_user_by_username(username: str):
    """
    Retrieves a user by their username.
    """
    db = get_database()
    user = await db[USER_COLLECTION].find_one({"username": username})
    return user

async def get_user_by_email(email: str):
    """
    Retrieves a user by their email.
    """
    db = get_database()
    user = await db[USER_COLLECTION].find_one({"email": email})
    return user

async def create_user(user_data: UserCreate) -> UserInDB:
    """
    Creates a new user in the database.
    """
    db = get_database()
    hashed_password = get_password_hash(user_data.password)
    
    user_in_db = UserInDB(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    
    await db[USER_COLLECTION].insert_one(user_in_db.model_dump())
    
    return user_in_db