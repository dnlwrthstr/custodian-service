import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    # API settings
    API_V1_STR: str = "/v1"
    PROJECT_NAME: str = "Custodian Service"

    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

    # MongoDB settings
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "custodian_service")

    # Kafka settings
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    KAFKA_TRANSACTION_TOPIC: str = os.getenv("KAFKA_TRANSACTION_TOPIC", "custodian.transactions")
    KAFKA_CUSTODIAN_TOPIC: str = os.getenv("KAFKA_CUSTODIAN_TOPIC", "custodian.custodian")
    KAFKA_ENABLED: bool = os.getenv("KAFKA_ENABLED", "True").lower() in ("true", "1", "t")

    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-development-only")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    class Config:
        case_sensitive = True

# Create settings instance
settings = Settings()
