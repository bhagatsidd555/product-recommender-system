"""
Run this once to populate the database with sample data.
Usage: python seed_data.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.product import Product
from app.models.interaction import Interaction

# Create all tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# ── USERS ──────────────────────────────────────────
users = [
    User(username="rahul_sharma", email="rahul@example.com", age=25, gender="M", location="Mumbai"),
    User(username="priya_patel",  email="priya@example.com",  age=22, gender="F", location="Pune"),
    User(username="amit_kumar",   email="amit@example.com",   age=30, gender="M", location="Delhi"),
    User(username="neha_joshi",   email="neha@example.com",   age=27, gender="F", location="Bangalore"),
    User(username="vikram_singh", email="vikram@example.com", age=35, gender="M", location="Chennai"),
]

# ── PRODUCTS ───────────────────────────────────────
products = [
    Product(name="Nike Air Max 270",       category="Footwear",     brand="Nike",        price=7999,  rating=4.5, tags="shoes running sports casual", description="Lightweight running shoe with air cushioning"),
    Product(name="Adidas Ultraboost 22",   category="Footwear",     brand="Adidas",      price=9999,  rating=4.7, tags="shoes running boost sports",   description="Premium running shoes with boost technology"),
    Product(name="Levi's 511 Slim Jeans",  category="Clothing",     brand="Levis",       price=2999,  rating=4.2, tags="jeans denim casual slim",       description="Slim fit stretch denim jeans"),
    Product(name="H&M Cotton T-Shirt",     category="Clothing",     brand="HM",          price=599,   rating=3.9, tags="tshirt casual cotton basic",    description="Basic cotton round neck t-shirt"),
    Product(name="Sony WH-1000XM5",        category="Electronics",  brand="Sony",        price=24999, rating=4.8, tags="headphones wireless audio",     description="Industry leading noise cancelling headphones"),
    Product(name="boAt Rockerz 450",       category="Electronics",  brand="boAt",        price=1499,  rating=4.1, tags="headphones wireless bluetooth", description="On-ear wireless headphones 15hr battery"),
    Product(name="Samsung Galaxy Buds2",   category="Electronics",  brand="Samsung",     price=5999,  rating=4.3, tags="earbuds wireless tws audio",    description="True wireless earbuds with ANC"),
    Product(name="The Alchemist",          category="Books",        brand="HarperCollins", price=299, rating=4.7, tags="novel fiction bestseller philosophy", description="Paulo Coelho's masterpiece"),
    Product(name="Atomic Habits",          category="Books",        brand="Penguin",     price=399,   rating=4.9, tags="self-help habits productivity", description="Build good habits break bad ones"),
    Product(name="Instant Pot Duo 7-in-1", category="Kitchen",     brand="InstantPot",  price=6499,  rating=4.6, tags="cooker pressure kitchen smart", description="7-in-1 multi-use pressure cooker"),
    Product(name="Prestige Iron Press",    category="Kitchen",      brand="Prestige",    price=1299,  rating=4.0, tags="iron press kitchen home",       description="1400W dry iron with steam"),
    Product(name="Wildcraft Backpack 30L", category="Sports",       brand="Wildcraft",   price=1799,  rating=4.2, tags="bag backpack travel outdoor",   description="30L water resistant backpack"),
]

# ── INTERACTIONS ───────────────────────────────────
interactions = [
    # Rahul - likes Footwear + Electronics
    Interaction(user_id=1, product_id=1, interaction_type="purchase", rating=5.0),
    Interaction(user_id=1, product_id=5, interaction_type="purchase", rating=4.5),
    Interaction(user_id=1, product_id=6, interaction_type="view"),
    Interaction(user_id=1, product_id=3, interaction_type="click"),

    # Priya - likes Books + Clothing
    Interaction(user_id=2, product_id=8, interaction_type="purchase", rating=5.0),
    Interaction(user_id=2, product_id=9, interaction_type="purchase", rating=4.8),
    Interaction(user_id=2, product_id=4, interaction_type="purchase", rating=4.0),
    Interaction(user_id=2, product_id=3, interaction_type="view"),

    # Amit - likes Electronics + Sports
    Interaction(user_id=3, product_id=5, interaction_type="purchase", rating=4.5),
    Interaction(user_id=3, product_id=7, interaction_type="purchase", rating=4.2),
    Interaction(user_id=3, product_id=12, interaction_type="wishlist"),
    Interaction(user_id=3, product_id=2, interaction_type="click"),

    # Neha - likes Clothing + Kitchen
    Interaction(user_id=4, product_id=4, interaction_type="purchase", rating=3.8),
    Interaction(user_id=4, product_id=10, interaction_type="purchase", rating=4.6),
    Interaction(user_id=4, product_id=11, interaction_type="view"),
    Interaction(user_id=4, product_id=8, interaction_type="view"),

    # Vikram - likes Footwear + Books + Sports
    Interaction(user_id=5, product_id=2, interaction_type="purchase", rating=4.7),
    Interaction(user_id=5, product_id=9, interaction_type="purchase", rating=5.0),
    Interaction(user_id=5, product_id=12, interaction_type="purchase", rating=4.3),
    Interaction(user_id=5, product_id=1, interaction_type="view"),
]

try:
    # Check if already seeded
    if db.query(User).count() > 0:
        print("⚠️  Database already has data. Skipping seed.")
    else:
        db.add_all(users)
        db.commit()
        print(f"✅ Added {len(users)} users")

        db.add_all(products)
        db.commit()
        print(f"✅ Added {len(products)} products")

        db.add_all(interactions)
        db.commit()
        print(f"✅ Added {len(interactions)} interactions")

        print("\n🎉 Database seeded successfully!")
        print("📌 Test URLs:")
        print("   http://localhost:8000/api/recommendations/1?strategy=hybrid")
        print("   http://localhost:8000/api/recommendations/2?strategy=content")
        print("   http://localhost:8000/api/recommendations/3?strategy=collaborative")
except Exception as e:
    db.rollback()
    print(f"❌ Error: {e}")
finally:
    db.close()