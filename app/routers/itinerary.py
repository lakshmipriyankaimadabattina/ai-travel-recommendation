from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.database import db

router = APIRouter()

class ItineraryRequest(BaseModel):
    destination_names: List[str]
    trip_length_days: int
    user_interests: List[str] = []

@router.post("/itinerary")
async def generate_itinerary(req: ItineraryRequest):
    days = []
    total_budget = 0.0
    days_per_dest = max(1, req.trip_length_days // len(req.destination_names))

    for i, dest_name in enumerate(req.destination_names):
        dest = await db.destinations.find_one({"name": dest_name})
        if not dest:
            continue
        activities = dest.get("activities", [])[:days_per_dest]
        total_budget += dest.get("avg_budget_usd", 0) * days_per_dest / 7

        for day_offset in range(days_per_dest):
            day_num = i * days_per_dest + day_offset + 1
            act = activities[day_offset] if day_offset < len(activities) else "explore"
            days.append({
                "day": day_num,
                "destination": dest_name,
                "activity": act,
                "notes": f"Day {day_num} in {dest['country']}",
            })

    return {"days": days, "total_budget_estimate_usd": round(total_budget, 2)}