from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.mongodb_url)
db = client[settings.database_name]

async def get_database():
    return db

async def close_mongo_connection():
    client.close()