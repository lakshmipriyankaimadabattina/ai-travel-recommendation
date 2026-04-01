import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def seed():
    client = AsyncIOMotorClient('mongodb://db:27017')
    db = client['travel_db']
    op = {'$set': {'password': 'pass123'}}
    await db.users.update_one({'username': 'alice'}, op, upsert=True)
    await db.users.update_one({'username': 'bob'}, op, upsert=True)
    print('Done')
    client.close()

asyncio.run(seed())
