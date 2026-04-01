from fastapi import APIRouter, HTTPException
from app.models.user import RegisterRequest, LoginRequest, UserResponse
from datetime import datetime, timezone
from app.database import db

router = APIRouter()


# ── Endpoints ──────────────────────────────────────────────────────────────

@router.post("/users/register", response_model=UserResponse)
async def register(req: RegisterRequest):
    existing = await db.users.find_one({"username": req.username.lower()})
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    user_doc = {
        "username": req.username.lower(),
        "name": req.name,
        "password": req.password,
        "interests": req.interests,
        "interaction_history": [],
        "preferences": {},
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.users.insert_one(user_doc)

    return UserResponse(
        username=req.username.lower(),
        name=req.name,
        interests=req.interests,
        interactions=0,
    )


@router.post("/users/login", response_model=UserResponse)
async def login(req: LoginRequest):
    user = await db.users.find_one({"username": req.username.lower()})
    if not user or user.get("password") != req.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return UserResponse(
        username=user["username"],
        name=user.get("name", user["username"]),
        interests=user.get("interests", []),
        interactions=len(user.get("interaction_history", [])),
    )


@router.post("/users/{username}/interaction")
async def log_interaction(username: str, destination_name: str, rating: float = 3.0):
    """Called after every search to increment interaction count in MongoDB."""
    await db.users.update_one(
        {"username": username.lower()},
        {"$push": {"interaction_history": {
            "destination_id": destination_name,
            "rating": rating,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }}}
    )
    user = await db.users.find_one({"username": username.lower()})
    return {"interactions": len(user.get("interaction_history", []))}


@router.get("/users/{username}", response_model=UserResponse)
async def get_user(username: str):
    user = await db.users.find_one({"username": username.lower()})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        username=user["username"],
        name=user.get("name", user["username"]),
        interests=user.get("interests", []),
        interactions=len(user.get("interaction_history", [])),
    )