import spacy
from typing import Dict

nlp = spacy.load("en_core_web_sm")

INTENT_KEYWORDS = {
    "destination_search": ["find","show","recommend","suggest","where"],
    "plan_trip":          ["plan","itinerary","trip","schedule"],
    "get_weather":        ["weather","temperature","forecast","climate"],
}
CATEGORY_WORDS = {
    "beach":    ["beach","ocean","sea","coastal","island"],
    "mountain": ["mountain","hiking","ski","skiing","alpine"],
    "city":     ["city","urban","shopping","nightlife"],
    "cultural": ["culture","history","museum","temple"],
}
CLIMATE_WORDS = {
    "tropical":  ["warm","hot","tropical","sunny"],
    "cold":      ["cold","snow","winter","freezing"],
    "temperate": ["mild","temperate","spring"],
}

def parse_query(text: str) -> Dict:
    doc = nlp(text.lower())
    tokens = [t.text for t in doc]

    # Classify intent
    intent = "out_of_scope"
    for name, keywords in INTENT_KEYWORDS.items():
        if any(k in tokens for k in keywords):
            intent = name; break

    # Extract entities using spaCy NER
    locations = [e.text for e in doc.ents if e.label_ in ["GPE","LOC"]]

    # Match category and climate from keywords
    category = None
    for cat, words in CATEGORY_WORDS.items():
        if any(w in tokens for w in words):
            category = cat; break

    climate = None
    for cli, words in CLIMATE_WORDS.items():
        if any(w in tokens for w in words):
            climate = cli; break

    # Extract budget numbers
    budget = None
    for token in doc:
        if token.like_num:
            budget = float(token.text.replace(",",""))

    return {
        "intent":    intent,
        "locations": locations,
        "category":  category,
        "climate":   climate,
        "budget":    budget,
        "raw_query": text,
    }