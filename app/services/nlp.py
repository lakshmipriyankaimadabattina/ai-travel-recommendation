import spacy
from typing import Dict

nlp = spacy.load("en_core_web_sm")

INTENT_KEYWORDS = {
    "destination_search": ["find", "show", "recommend", "suggest", "where"],
    "plan_trip": ["plan", "trip", "itinerary", "schedule"],
    "weather": ["weather", "temperature", "forecast"]
}

CATEGORY_WORDS = {
    "beach": ["beach", "ocean", "sea", "island"],
    "mountain": ["mountain", "hiking", "ski"],
    "city": ["city", "urban", "shopping"],
    "cultural": ["culture", "history", "museum", "temple"]
}

CLIMATE_WORDS = {
    "tropical": ["warm", "hot", "sunny"],
    "cold": ["cold", "snow", "winter"],
    "temperate": ["mild", "spring"]
}


def parse_query(text: str) -> Dict:
    doc = nlp(text.lower())
    tokens = [t.text for t in doc]

    intent = "unknown"
    for key, words in INTENT_KEYWORDS.items():
        if any(w in tokens for w in words):
            intent = key
            break

    category = None
    for cat, words in CATEGORY_WORDS.items():
        if any(w in tokens for w in words):
            category = cat

    climate = None
    for cli, words in CLIMATE_WORDS.items():
        if any(w in tokens for w in words):
            climate = cli

    budget = None
    for token in doc:
        if token.like_num:
            budget = float(token.text)

    return {
        "intent": intent,
        "category": category,
        "climate": climate,
        "budget": budget,
        "raw": text
    }