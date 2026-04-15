from sqlalchemy.orm import Session
from .collaborative_filter import collaborative_filtering
from .content_based import content_based_filtering

def hybrid_recommendations(user_id: int, db: Session, top_n: int = 10):
    """
    Hybrid Recommendation Strategy
    - Combines Collaborative Filtering + Content-Based Filtering
    - Weighted scoring: CF (60%) + CBF (40%)
    - Deduplicates and returns top N
    """
    cf_results = collaborative_filtering(user_id, db, top_n=top_n)
    cb_results = content_based_filtering(user_id, db, top_n=top_n)

    # Score products
    scores = {}

    # CF weighted at 0.6
    for rank, product in enumerate(cf_results):
        score = (top_n - rank) * 0.6
        scores[product.id] = {"product": product, "score": scores.get(product.id, {}).get("score", 0) + score}

    # CB weighted at 0.4
    for rank, product in enumerate(cb_results):
        score = (top_n - rank) * 0.4
        if product.id in scores:
            scores[product.id]["score"] += score
        else:
            scores[product.id] = {"product": product, "score": score}

    # Sort by combined score
    sorted_products = sorted(scores.values(), key=lambda x: x["score"], reverse=True)
    return [item["product"] for item in sorted_products[:top_n]]