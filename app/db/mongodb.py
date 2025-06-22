from motor.motor_asyncio import AsyncIOMotorClient
from typing import AsyncGenerator, Optional
import asyncio
import logging
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB client and database instances
client: Optional[AsyncIOMotorClient] = None
database = None

# Collections
custodian_collection = None
portfolio_collection = None
account_collection = None
position_collection = None
transaction_collection = None

async def connect_to_mongodb(max_retries=5, retry_delay=5):
    """
    Establish connection to MongoDB with retry mechanism.

    Args:
        max_retries: Maximum number of connection attempts
        retry_delay: Delay between retries in seconds
    """
    global client, database, custodian_collection, portfolio_collection, account_collection, position_collection, transaction_collection

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Attempting to connect to MongoDB at {settings.MONGODB_URL} (Attempt {attempt}/{max_retries})")
            client = AsyncIOMotorClient(
                settings.MONGODB_URL,
                serverSelectionTimeoutMS=5000  # 5 second timeout for server selection
            )

            # Force a connection to verify it works
            await client.admin.command('ping')

            database = client[settings.MONGODB_DB_NAME]

            # Initialize collections
            custodian_collection = database.custodians
            portfolio_collection = database.portfolios
            account_collection = database.accounts
            position_collection = database.positions
            transaction_collection = database.transactions

            logger.info("Successfully connected to MongoDB")
            return
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            if attempt < max_retries:
                logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                logger.error(f"Failed to connect to MongoDB after {max_retries} attempts")
                raise

async def get_database() -> AsyncGenerator:
    """
    Get MongoDB database connection.

    Ensures that a connection to MongoDB exists before yielding the database.
    """
    if client is None:
        await connect_to_mongodb()

    try:
        yield database
    except Exception as e:
        logger.error(f"Error during database operation: {str(e)}")
        raise
    finally:
        # No need to close the connection as Motor manages the connection pool
        pass
