from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    category: str
    sub_category: Optional[str] = None
    brand: Optional[str] = None
    price: float
    rating: Optional[float] = 0.0
    description: Optional[str] = None
    tags: Optional[str] = None
    image_url: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    sub_category: Optional[str]
    brand: Optional[str]
    price: float
    rating: Optional[float]
    description: Optional[str]
    tags: Optional[str]
    image_url: Optional[str]

    class Config:
        from_attributes = True