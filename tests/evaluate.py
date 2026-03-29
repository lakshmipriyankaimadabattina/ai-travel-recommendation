# Define ground truth: for each user, which destinations are "relevant"?
GROUND_TRUTH = {
    "alice": ["Bali", "Maldives"],
    "bob":   ["Paris", "Tokyo"],
}

def precision_at_k(recommended, relevant, k):
    top_k = recommended[:k]
    hits = sum(1 for r in top_k if r in relevant)
    return hits / k

def recall_at_k(recommended, relevant, k):
    top_k = recommended[:k]
    hits = sum(1 for r in top_k if r in relevant)
    return hits / len(relevant) if relevant else 0

def f1_score(p, r):
    return 2 * p * r / (p + r) if (p + r) > 0 else 0

def evaluate(recommended_names, username, k=5):
    relevant = GROUND_TRUTH.get(username, [])
    p = precision_at_k(recommended_names, relevant, k)
    r = recall_at_k(recommended_names, relevant, k)
    f1 = f1_score(p, r)
    print(f"Precision@{k}: {p:.3f} | Recall@{k}: {r:.3f} | F1: {f1:.3f}")
    return {"precision": p, "recall": r, "f1": f1}

# Run evaluation for Alice
if __name__ == "__main__":
    alice_recommendations = ["Maldives", "Bali", "Paris", "Tokyo", "Patagonia"]
    print("Alice evaluation:")
    evaluate(alice_recommendations, "alice", k=5)

    bob_recommendations = ["Paris", "Tokyo", "Bali", "Maldives", "Patagonia"]
    print("Bob evaluation:")
    evaluate(bob_recommendations, "bob", k=5)
