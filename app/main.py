from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import close_mongo_connection
from app.routers import recommend, query, itinerary, weather

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_mongo_connection()

app = FastAPI(
    title="AI Travel Recommendation API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(recommend.router, prefix="/api")
app.include_router(query.router, prefix="/api")
app.include_router(itinerary.router, prefix="/api")
app.include_router(weather.router, prefix="/api")

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def root():
    return {"message": "AI Travel Recommendation API is running"}