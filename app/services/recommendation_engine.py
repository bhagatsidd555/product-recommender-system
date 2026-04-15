from sqlalchemy.orm import Session
from .collaborative_filter import collaborative_filtering
from .content_based import content_based_filtering
from .hybrid import hybrid_recommendations

def get_recommendations(user_id: int, strategy: str, db: Session, top_n: int = 10):
    """
    Main recommendation engine dispatcher
    Strategies: 'collaborative', 'content', 'hybrid'
    """
    if strategy == "collaborative":
        return collaborative_filtering(user_id, db, top_n)
    elif strategy == "content":
        return content_based_filtering(user_id, db, top_n)
    else:
        return hybrid_recommendations(user_id, db, top_n)