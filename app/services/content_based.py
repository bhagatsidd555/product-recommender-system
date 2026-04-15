import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from ..models.product import Product
from ..models.interaction import Interaction

def build_product_features(product: Product) -> str:
    """Combine product features into a single text for TF-IDF"""
    parts = [
        product.category or "",
        product.sub_category or "",
        product.brand or "",
        product.tags or "",
        product.description or ""
    ]
    return " ".join(filter(None, parts)).lower()

def content_based_filtering(user_id: int, db: Session, top_n: int = 10):
    """
    Content-Based Filtering
    - Builds TF-IDF vectors for all products
    - Finds products similar to what user has interacted with
    - Recommends most similar unseen products
    """
    all_products = db.query(Product).all()

    if not all_products:
        return []

    # Build product feature corpus
    product_ids = [p.id for p in all_products]
    product_features = [build_product_features(p) for p in all_products]

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words="english", max_features=500)
    tfidf_matrix = vectorizer.fit_transform(product_features)
    
    # Cosine similarity between all products
    similarity_matrix = cosine_similarity(tfidf_matrix)
    similarity_df = pd.DataFrame(similarity_matrix, index=product_ids, columns=product_ids)

    # Get products user has interacted with
    user_interactions = db.query(Interaction).filter(Interaction.user_id == user_id).all()
    
    if not user_interactions:
        # Cold start: return top-rated products by category diversity
        return db.query(Product).order_by(Product.rating.desc()).limit(top_n).all()

    interacted_product_ids = list(set([i.product_id for i in user_interactions]))

    # Score products based on similarity to interacted ones
    candidate_scores = {}
    for pid in interacted_product_ids:
        if pid not in similarity_df.index:
            continue
        similar_prods = similarity_df[pid].drop(interacted_product_ids, errors='ignore')
        for prod_id, score in similar_prods.items():
            if prod_id not in candidate_scores:
                candidate_scores[prod_id] = 0
            candidate_scores[prod_id] += score

    top_product_ids = sorted(candidate_scores, key=candidate_scores.get, reverse=True)[:top_n]
    products = db.query(Product).filter(Product.id.in_(top_product_ids)).all()
    return products