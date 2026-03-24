import os
from typing import Optional

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/stellar_spark")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "stellar-spark-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    def __init__(self):
        pass

settings = Settings()
