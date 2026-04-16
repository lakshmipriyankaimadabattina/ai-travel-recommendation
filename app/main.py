from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import close_mongo_connection
from app.routers import recommend, query, itinerary, weather
from fastapi.staticfiles import StaticFiles

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_mongo_connection()

app = FastAPI(
    title="AI Travel Recommendation API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(recommend.router, prefix="/api", tags=["recommendations"])
app.include_router(query.router, prefix="/api", tags=["query"])
app.include_router(itinerary.router, prefix="/api", tags=["itinerary"])
app.include_router(weather.router, prefix="/api", tags=["weather"])

@app.get("/")
async def root():
    return {"message": "AI Travel API is running"}

@app.get("/health")
async def health():
    return {"status": "ok"}
