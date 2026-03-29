from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class Destination(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    country: str
    category: str           # beach, city, mountain, cultural
    climate: str            # tropical, temperate, arid, cold
    avg_budget_usd: float
    activities: List[str]
    description: str
    feature_vector: Optional[List[float]] = None

    class Config:
        populate_by_name = True