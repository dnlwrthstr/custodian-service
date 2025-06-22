import uvicorn
import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.core.config import settings
from app.db.mongodb import connect_to_mongodb, get_database

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
        # We don't raise the exception here to allow the application to start
        # even if the database is not available initially. It will retry on requests.

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connection on shutdown."""
    logger.info("Closing MongoDB connection...")
    # Motor handles connection pooling, so explicit closing is not required

@app.get("/", tags=["Health Check"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "custodian-service"}

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
