"""
Seeds demo users alice and bob into MongoDB.
Run once before demo:  python data/seed_users.py
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

DEMO_USERS = [
    {
        "username": "alice",
        "name": "Alice Chen",
        "password": "pass123",
        "interests": ["Beach", "Culture", "Food", "Luxury"],
        "interaction_history": [
            {"destination_id": "Bali",      "rating": 5.0, "timestamp": "2025-01-01T00:00:00"},
            {"destination_id": "Maldives",  "rating": 4.5, "timestamp": "2025-01-02T00:00:00"},
            {"destination_id": "Paris",     "rating": 4.0, "timestamp": "2025-01-03T00:00:00"},
            {"destination_id": "Tokyo",     "rating": 4.5, "timestamp": "2025-01-04T00:00:00"},
            {"destination_id": "Rome",      "rating": 4.0, "timestamp": "2025-01-05T00:00:00"},
            {"destination_id": "Santorini", "rating": 5.0, "timestamp": "2025-01-06T00:00:00"},
            {"destination_id": "Singapore", "rating": 3.5, "timestamp": "2025-01-07T00:00:00"},
            {"destination_id": "Kyoto",     "rating": 4.5, "timestamp": "2025-01-08T00:00:00"},
        ],
        "preferences": {"Beach": 0.9, "Culture": 0.7, "Food": 0.8, "Luxury": 0.85},
    },
    {
        "username": "bob",
        "name": "Bob Kumar",
        "password": "pass123",
        "interests": ["Adventure", "Nature", "History"],
        "interaction_history": [
            {"destination_id": "Nepal",     "rating": 5.0, "timestamp": "2025-01-01T00:00:00"},
            {"destination_id": "Patagonia", "rating": 4.5, "timestamp": "2025-01-02T00:00:00"},
        ],
        "preferences": {"Adventure": 0.9, "Nature": 0.8, "History": 0.7},
    },
]


async def seed():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["travel_db"]

    for user in DEMO_USERS:
        existing = await db.users.find_one({"username": user["username"]})
        if existing:
            print(f"  skip  '{user['username']}' — already exists")
        else:
            await db.users.insert_one(dict(user))
            n = len(user["interaction_history"])
            print(f"  added '{user['username']}' ({n} interactions)")

    client.close()
    print("Done.")


asyncio.run(seed())
