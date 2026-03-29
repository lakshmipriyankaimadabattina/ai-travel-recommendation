from fastapi import APIRouter, Query
from app.database import db
from app.services.recommender import hybrid_recommend

router = APIRouter()

@router.get("/recommend/{username}")
async def get_recommendations(username: str, top_k: int = Query(5, ge=1, le=20)):
    user = await db.users.find_one({"username": username})
    if not user:
        return {"error": "User not found"}

    destinations = await db.destinations.find().to_list(100)
    all_users = await db.users.find().to_list(1000)

    results = hybrid_recommend(user, all_users, destinations, top_k)

    # Convert ObjectId and numpy floats to JSON-serializable types
    clean_results = []
    for r in results:
        clean_results.append({
            "name": r["name"],
            "country": r["country"],
            "category": r["category"],
            "climate": r["climate"],
            "avg_budget_usd": r["avg_budget_usd"],
            "activities": r["activities"],
            "description": r["description"],
            "score": float(r["score"])
        })

    return {"username": username, "recommendations": clean_results}


