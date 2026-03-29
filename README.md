# AI Travel Recommendation System

An AI-powered travel recommendation system that combines content-based and collaborative filtering with NLP query parsing, weather integration, and itinerary generation.

## Live Demo
- API: https://ai-travel-recommendation.onrender.com/docs
- Recommendations: https://ai-travel-recommendation.onrender.com/api/recommend/alice

## Features
- Hybrid ML recommendation engine (content-based + collaborative filtering)
- NLP query parsing using spaCy
- Real-time weather data via OpenWeatherMap
- Itinerary generator
- Docker containerized
- CI/CD via GitHub Actions

## Setup Instructions

### 1. Clone the repo
```
git clone https://github.com/lakshmipriyankaimadabattina/ai-travel-recommendation.git
cd ai-travel-recommendation
```

### 2. Create virtual environment
```
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Set up environment variables
```
cp .env.example .env
# Edit .env with your values
```

### 5. Run locally
```
uvicorn app.main:app --reload --port 8001
```

## Environment Variables
| Key | Description |
|-----|-------------|
| `MONGODB_URL` | MongoDB connection string |
| `DATABASE_NAME` | Database name (travel_db) |
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key |

## API Documentation
Visit `/docs` endpoint for full interactive API documentation.

## Evaluation Results
| Metric | Alice | Bob |
|--------|-------|-----|
| Precision@5 | 0.400 | 0.400 |
| Recall@5 | 1.000 | 1.000 |
| F1@5 | 0.571 | 0.571 |
