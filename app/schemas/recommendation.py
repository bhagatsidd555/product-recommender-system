from pydantic import BaseModel, Field
from typing import List, Optional
from .product import ProductResponse


# ----------------------------------
# Recommendation Response Schema
# ----------------------------------
class RecommendationResponse(BaseModel):
    user_id: int = Field(..., example=1)
    strategy: str = Field(..., example="hybrid")
    recommendations: List[ProductResponse]


# ----------------------------------
# Interaction Create Schema
# ----------------------------------
class InteractionCreate(BaseModel):
    user_id: int = Field(..., example=1)
    product_id: int = Field(..., example=101)
    interaction_type: str = Field(
        ...,
        example="view",
        description="Type of interaction: view, click, purchase, wishlist, rating"
    )
    rating: Optional[float] = Field(
        None,
        ge=0,
        le=5,
        example=4.5,
        description="Rating value (0 to 5), only for rating interaction"
    )


# ----------------------------------
# Optional: Recommendation Request
# (Better API design 🔥)
# ----------------------------------
class RecommendationRequest(BaseModel):
    user_id: int = Field(..., example=1)
    strategy: str = Field(
        default="hybrid",
        example="content",
        description="Recommendation strategy: content, collaborative, hybrid"
    )
    top_n: int = Field(
        default=10,
        ge=1,
        le=50,
        example=10,
        description="Number of recommendations"
    )


# ----------------------------------
# Optional: Simple Response Message
# ----------------------------------
class MessageResponse(BaseModel):
    message: str
    status: str = "success"