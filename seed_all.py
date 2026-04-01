import asyncio, json
from motor.motor_asyncio import AsyncIOMotorClient

async def seed():
    client = AsyncIOMotorClient('mongodb://db:27017')
    db = client['travel_db']
    with open('/app/data/seed_destinations.json') as f:
        dests = json.load(f)
    await db.destinations.delete_many({})
    await db.destinations.insert_many(dests)
    print(f'Seeded {len(dests)} destinations')
    client.close()

asyncio.run(seed())
