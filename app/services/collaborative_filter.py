import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from ..models.interaction import Interaction
from ..models.product import Product

def get_interaction_weight(interaction_type: str) -> float:
    """Assign weight based on interaction type"""
    weights = {
        "view": 1.0,
        "click": 2.0,
        "wishlist": 3.0,
        "rating": 4.0,
        "purchase": 5.0
    }
    return weights.get(interaction_type, 1.0)

def collaborative_filtering(user_id: int, db: Session, top_n: int = 10):
    """
    User-Based Collaborative Filtering
    - Builds user-item matrix
    - Finds similar users using cosine similarity
    - Recommends products liked by similar users
    """
    interactions = db.query(Interaction).all()

    if not interactions:
        return []

    # Build weighted user-item matrix
    data = []
    for i in interactions:
        weight = get_interaction_weight(i.interaction_type)
        if i.rating:
            weight = i.rating  # Use actual rating if available
        data.append({"user_id": i.user_id, "product_id": i.product_id, "score": weight})

    df = pd.DataFrame(data)
    
    # Pivot to user-item matrix
    user_item_matrix = df.pivot_table(
        index="user_id", 
        columns="product_id", 
        values="score", 
        aggfunc="max",
        fill_value=0
    )

    if user_id not in user_item_matrix.index:
        # Cold Start: return top-rated products
        return cold_start_recommendations(db, top_n)

    # Cosine similarity between users
    from sklearn.metrics.pairwise import cosine_similarity
    similarity_matrix = cosine_similarity(user_item_matrix)
    similarity_df = pd.DataFrame(
        similarity_matrix,
        index=user_item_matrix.index,
        columns=user_item_matrix.index
    )

    # Get most similar users (exclude self)
    similar_users = similarity_df[user_id].drop(user_id).sort_values(ascending=False).head(10).index.tolist()

    if not similar_users:
        return cold_start_recommendations(db, top_n)

    # Products already interacted with by current user
    seen_products = set(user_item_matrix.loc[user_id][user_item_matrix.loc[user_id] > 0].index.tolist())

    # Aggregate scores from similar users
    candidate_scores = {}
    for sim_user in similar_users:
        sim_score = similarity_df.loc[user_id, sim_user]
        user_products = user_item_matrix.loc[sim_user]
        for prod_id, rating in user_products.items():
            if rating > 0 and prod_id not in seen_products:
                if prod_id not in candidate_scores:
                    candidate_scores[prod_id] = 0
                candidate_scores[prod_id] += sim_score * rating

    # Sort by score and get top N
    top_product_ids = sorted(candidate_scores, key=candidate_scores.get, reverse=True)[:top_n]
    
    products = db.query(Product).filter(Product.id.in_(top_product_ids)).all()
    return products

def cold_start_recommendations(db: Session, top_n: int = 10):
    """Fallback for new users: return highest rated products"""
    return db.query(Product).order_by(Product.rating.desc()).limit(top_n).all()