from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from ..database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)
    sub_category = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    rating = Column(Float, default=0.0)
    description = Column(Text, nullable=True)
    tags = Column(String, nullable=True)  # comma-separated tags
    image_url = Column(String, nullable=True)

    interactions = relationship("Interaction", back_populates="product")