from pydantic import BaseModel
from typing import List, Optional

class ItineraryDay(BaseModel):
    day: int
    destination: str
    activities: List[str]
    notes: str

class Itinerary(BaseModel):
    user_id: str
    title: str
    trip_length_days: int
    total_budget_usd: float
    days: List[ItineraryDay]
    created_at: Optional[str] = None