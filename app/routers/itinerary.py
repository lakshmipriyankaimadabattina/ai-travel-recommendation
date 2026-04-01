from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.database import db

router = APIRouter()


class ItineraryRequest(BaseModel):
    destinations: List[str]
    days: int
    interests: List[str] = []


def adjust_activities(activities, interests):
    if "relaxation" in interests:
        return activities[:2]
    elif "adventure" in interests:
        return activities[:5]
    return activities[:3]


@router.post("/itinerary")
async def generate_itinerary(req: ItineraryRequest):
    result = []
    day_count = 1

    for dest_name in req.destinations:
        dest = await db.destinations.find_one({"name": dest_name})
        if not dest:
            continue

        acts = adjust_activities(dest["activities"], req.interests)

        for act in acts:
            result.append({
                "day": day_count,
                "destination": dest_name,
                "activity": act
            })
            day_count += 1

    return {"plan": result}