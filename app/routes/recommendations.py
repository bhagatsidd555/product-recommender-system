from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..models.interaction import Interaction
from ..schemas.recommendation import RecommendationResponse, InteractionCreate
from ..schemas.product import ProductResponse
from ..services.recommendation_engine import get_recommendations
from typing import List

router = APIRouter()

@router.get("/{user_id}", response_model=RecommendationResponse)
def recommend_for_user(
    user_id: int,
    strategy: str = Query(default="hybrid", enum=["collaborative", "content", "hybrid"]),
    top_n: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    products = get_recommendations(user_id, strategy, db, top_n)

    return RecommendationResponse(
        user_id=user_id,
        strategy=strategy,
        recommendations=products
    )

@router.post("/interact")
def log_interaction(interaction: InteractionCreate, db: Session = Depends(get_db)):
    """Log user-product interaction (view, click, purchase, rating, etc.)"""
    db_interaction = Interaction(**interaction.dict())
    db.add(db_interaction)
    db.commit()
    return {"message": "Interaction logged successfully"}