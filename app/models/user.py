from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class UserInteraction(BaseModel):
    destination_id: str
    rating: float       # 1.0 to 5.0
    timestamp: str

class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    username: str
    email: str
    preferences: Dict[str, float] = {}  # {"beach": 0.8, "mountain": 0.3}
    interaction_history: List[UserInteraction] = []

    class Config:
        populate_by_name = True