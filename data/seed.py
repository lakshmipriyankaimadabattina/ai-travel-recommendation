import asyncio, json
from motor.motor_asyncio import AsyncIOMotorClient

async def seed():
    print("Starting seed script...")
    client = AsyncIOMotorClient("mongodb+srv://ilpriyanka153_db_user:Shalu2063@cluster0.wugvfuk.mongodb.net/?appName=Cluster0")
    db = client["travel_db"]
    print("Connected to MongoDB!")

    with open("data/seed_destinations.json") as f:
        destinations = json.load(f)
    await db.destinations.delete_many({})
    await db.destinations.insert_many(destinations)
    print(f"Seeded {len(destinations)} destinations successfully!")

    with open("data/seed_users.json") as f:
        users = json.load(f)
    await db.users.delete_many({})
    await db.users.insert_many(users)
    print(f"Seeded {len(users)} users successfully!")

    client.close()

asyncio.run(seed())
