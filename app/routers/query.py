from fastapi import APIRouter
from pydantic import BaseModel
from app.services.nlp import parse_query
from app.services.recommender import hybrid_recommend
from app.database import db

router = APIRouter()

class QueryRequest(BaseModel):
    text: str

@router.post("/smart-search")
async def smart_search(req: QueryRequest):
    try:
        parsed = parse_query(req.text)
        destinations = await db.destinations.find().to_list(100)
        user = {
            "category": parsed.get("category") or "beach",
            "climate": parsed.get("climate") or "tropical",
            "avg_budget_usd": parsed.get("budget") or 2000
        }
        results = hybrid_recommend(user, parsed, destinations)
        clean = []
        for r in results:
            clean.append({
                "name": r.get("name", ""),
                "country": r.get("country", ""),
                "category": r.get("category", ""),
                "climate": r.get("climate", ""),
                "avg_budget_usd": r.get("avg_budget_usd", 0),
                "activities": r.get("activities", []),
                "description": r.get("description", ""),
                "score": float(r.get("score", 0))
            })
        return {"parsed": parsed, "recommendations": clean}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise
