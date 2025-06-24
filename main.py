import uvicorn
import logging
import os
import sys
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.core.config import settings
from app.db.mongodb import connect_to_mongodb, get_database
from app.db.kafka import connect_to_kafka, close_kafka_connection, get_kafka_service

# Import the seed_database function
sys_path = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(sys_path, "data")
sys.path.append(data_dir)
from seed_database import seed_database

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Custodian Service API",
    description="""
    API for custodian services implementing OpenWealth standards.

    ## Features

    * Manage custodians and their credentials
    * Track portfolios, accounts, positions, and transactions
    * Implement OpenWealth standards for financial data

    ## API Documentation

    * Swagger UI: `/docs`
    * ReDoc: `/redoc`
    * OpenAPI JSON: `/openapi.json`
    """,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")

@app.on_event("startup")
async def startup_db_client():
    """Initialize database connection on startup."""
    logger.info("Connecting to MongoDB...")
    try:
        await connect_to_mongodb()
        logger.info("MongoDB connection established")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        # Fail fast: If we can't connect to the database, the application should not start
        # as it cannot fulfill its primary function
        raise

@app.on_event("startup")
async def startup_kafka_client():
    """Initialize Kafka connection on startup."""
    if settings.KAFKA_ENABLED:
        logger.info("Connecting to Kafka...")
        # connect_to_kafka now handles exceptions internally
        kafka_service = await connect_to_kafka()
        if kafka_service:
            logger.info("Kafka connection established")
        else:
            logger.warning("Failed to establish Kafka connection during startup. Will retry when needed.")
            # The application can still function without Kafka
            # The get_kafka_service function will retry connecting when needed

@app.on_event("startup")
async def seed_database_on_startup():
    """Seed the database with initial data on startup."""
    logger.info("Seeding database with initial data...")
    try:
        await seed_database()
        logger.info("Database seeding completed successfully")
    except Exception as e:
        logger.error(f"Failed to seed database: {str(e)}")
        # Log error but don't fail the application startup
        # The application can still function with an empty database

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connection on shutdown."""
    logger.info("Closing MongoDB connection...")
    # Motor handles connection pooling, so explicit closing is not required

@app.on_event("shutdown")
async def shutdown_kafka_client():
    """Close Kafka connection on shutdown."""
    if settings.KAFKA_ENABLED:
        logger.info("Closing Kafka connection...")
        await close_kafka_connection()

@app.get("/", tags=["Health Check"])
async def health_check():
    """Health check endpoint"""
    # Since we're using the fail-fast approach, if this endpoint is reachable,
    # it means the application has started successfully and the database connection is available
    return {"status": "healthy", "service": "custodian-service", "database": "connected"}

@app.get("/db-health", tags=["Health Check"])
async def db_health_check(db = Depends(get_database)):
    """Database health check endpoint"""
    try:
        # Simple ping to check if database is responsive
        await db.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
