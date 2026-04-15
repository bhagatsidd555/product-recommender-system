from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .database import Base, engine
from .routes import users, products, recommendations


# -------------------------------
# Lifespan Event (Better than startup)
# -------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("🚀 Starting Product Recommender System...")

    # Create DB tables
    Base.metadata.create_all(bind=engine)

    yield

    # Shutdown logic
    print("🛑 Shutting down application...")


# -------------------------------
# App Initialization
# -------------------------------
app = FastAPI(
    title="Product Recommender System",
    description="AI-powered personalized product recommendation engine",
    version="1.0.0",
    lifespan=lifespan
)


# -------------------------------
# CORS Middleware
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------
# Routes Registration
# -------------------------------
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])


# -------------------------------
# Health Check
# -------------------------------
@app.get("/")
def root():
    return {
        "message": "🚀 Product Recommender System API is running",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "Product Recommender API"
    }
print("all well")