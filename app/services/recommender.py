import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def build_vector(dest):
    categories = ["beach", "city", "mountain", "cultural", "adventure"]
    climates = ["tropical", "temperate", "cold", "arid"]
    cat = dest.get("category", "").lower()
    cli = dest.get("climate", "").lower()
    cat_vec = [1 if cat == c else 0 for c in categories]
    cli_vec = [1 if cli == c else 0 for c in climates]
    budget = [dest.get("avg_budget_usd", 1000) / 5000]
    return cat_vec + cli_vec + budget

def content_score(user_pref, destinations):
    user_vec = np.array([build_vector(user_pref)])
    scores = {}
    for d in destinations:
        d_vec = np.array([build_vector(d)])
        sim = cosine_similarity(user_vec, d_vec)[0][0]
        scores[d["name"]] = sim
    return scores

def apply_nlp_boost(destinations, parsed):
    scores = {}
    for d in destinations:
        score = 0
        if parsed.get("category") and parsed["category"].lower() == d.get("category", "").lower():
            score += 0.4
        if parsed.get("climate") and parsed["climate"].lower() == d.get("climate", "").lower():
            score += 0.3
        budget = parsed.get("budget")
        if budget:
            if d.get("avg_budget_usd", 0) <= budget:
                score += 0.3
            else:
                score -= 0.2
        scores[d["name"]] = score
    return scores

def hybrid_recommend(user, parsed, destinations, top_k=5):
    if not destinations:
        return []
    cb_scores = content_score(user, destinations)
    nlp_scores = apply_nlp_boost(destinations, parsed)
    results = []
    for d in destinations:
        score = cb_scores.get(d["name"], 0) + nlp_scores.get(d["name"], 0)
        results.append({**d, "score": round(score, 3)})
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]
