from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.database import close_mongo_connection
from app.routers import recommend, query, itinerary, weather, users

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_mongo_connection()

app = FastAPI(
    title="AI Travel Recommendation API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(users,     prefix="/api", tags=["users"])
app.include_router(recommend, prefix="/api", tags=["recommendations"])
app.include_router(query,     prefix="/api", tags=["query"])
app.include_router(itinerary, prefix="/api", tags=["itinerary"])
app.include_router(weather,   prefix="/api", tags=["weather"])

app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

@app.get("/health")
async def health():
    return {"message": "AI Travel API is running"}
