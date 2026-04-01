from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class RegisterRequest(BaseModel):
    username: str
    name: str
    password: str
    interests: List[str] = []


class LoginRequest(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    username: str
    name: str
    interests: List[str]
    interactions: int


class User(BaseModel):
    username: str
    name: str
    password: str
    interests: List[str] = []
    interaction_history: List[dict] = []
    preferences: dict = {}
    created_at: Optional[str] = None