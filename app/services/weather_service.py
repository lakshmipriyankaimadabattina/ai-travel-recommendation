import requests, time
from app.config import settings

_cache: dict = {}
CACHE_TTL = 3600  # 1 hour

def get_weather(city: str) -> dict:
    now = time.time()
    if city in _cache and now - _cache[city]["ts"] < CACHE_TTL:
        return _cache[city]["data"]

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": settings.openweather_api_key,
              "units": "metric"}
    try:
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        data = r.json()
        result = {
            "city":        data["name"],
            "temp_c":      data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity":    data["main"]["humidity"],
        }
        _cache[city] = {"data": result, "ts": now}
        return result
    except Exception as e:
        return {"error": "Weather unavailable", "detail": str(e)}