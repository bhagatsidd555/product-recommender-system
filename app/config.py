class Settings:
    APP_NAME: str = "Product Recommender System"
    DATABASE_URL: str = "sqlite:///./recommender.db"
    TOP_N_RECOMMENDATIONS: int = 10

settings = Settings()