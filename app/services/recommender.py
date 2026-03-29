import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict

CATEGORIES     = ["beach", "city", "mountain", "cultural", "adventure"]
CLIMATES       = ["tropical", "temperate", "arid", "cold"]
ALL_ACTIVITIES = ["surfing","temples","yoga","snorkeling","museums",
                  "dining","shopping","history","hiking","skiing",
                  "wildlife","photography","food","diving","relaxation"]

def build_feature_vector(obj: dict) -> List[float]:
    # Works for both destinations and user preferences
    cat    = [1.0 if obj.get("category") == c else 0.0 for c in CATEGORIES]
    cli    = [1.0 if obj.get("climate") == c else 0.0 for c in CLIMATES]
    budget = [min(obj.get("avg_budget_usd", 0) / 5000.0, 1.0)]
    acts   = [1.0 if a in obj.get("activities", []) else 0.0 for a in ALL_ACTIVITIES]
    return cat + cli + budget + acts

def content_based_rank(user_prefs: dict, destinations: List[dict]) -> List[tuple]:
    dest_vectors = np.array([build_feature_vector(d) for d in destinations])
    user_vector  = np.array([build_feature_vector(user_prefs)]).reshape(1, -1)
    scores = cosine_similarity(user_vector, dest_vectors)[0]
    ranked = sorted(zip([d["name"] for d in destinations], scores),
                    key=lambda x: x[1], reverse=True)
    return ranked

def collaborative_rank(user_id: str, all_users: List[dict],
                       destinations: List[dict]) -> List[tuple]:
    dest_names = [d["name"] for d in destinations]
    matrix = {}
    for u in all_users:
        row = {d: 0.0 for d in dest_names}
        for interaction in u.get("interaction_history", []):
            if interaction.get("destination_id") in row:
                row[interaction["destination_id"]] = interaction["rating"]
        matrix[u["username"]] = row

    if user_id not in matrix or not matrix:
        return [(d, 0.0) for d in dest_names]

    target = np.array([matrix[user_id][d] for d in dest_names]).reshape(1, -1)
    others = np.array([[matrix[u][d] for d in dest_names]
                       for u in matrix if u != user_id])

    if len(others) == 0:
        return [(d, 0.0) for d in dest_names]

    sims = cosine_similarity(target, others)[0]
    weighted_scores = others.T @ sims
    total_sim = sum(sims) or 1.0
    scores = weighted_scores / total_sim

    ranked = sorted(zip(dest_names, scores),
                    key=lambda x: x[1], reverse=True)
    return ranked

def hybrid_recommend(user: dict, all_users: List[dict],
                     destinations: List[dict], top_k: int = 5) -> List[dict]:
    n_interactions = len(user.get("interaction_history", []))
    alpha = min(1.0, n_interactions / 20.0)

    user_prefs = user.get("preferences", {})

    cb_scores = dict(content_based_rank(user_prefs, destinations))
    cf_scores = dict(collaborative_rank(
        user["username"], all_users, destinations))

    results = []
    for dest in destinations:
        name = dest["name"]
        score = (alpha * cf_scores.get(name, 0.0) +
                 (1 - alpha) * cb_scores.get(name, 0.0))
        results.append({**dest, "score": round(score, 4)})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]
