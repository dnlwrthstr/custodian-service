from motor.motor_asyncio import AsyncIOMotorClient
from typing import AsyncGenerator

from app.core.config import settings

# MongoDB client instance
client = AsyncIOMotorClient(settings.MONGODB_URL)
database = client[settings.MONGODB_DB_NAME]

async def get_database() -> AsyncGenerator:
    """
    Get MongoDB database connection.
    """
    try:
        yield database
    finally:
        # No need to close the connection as Motor manages the connection pool
        pass

# Collections
custodian_collection = database.custodians
portfolio_collection = database.portfolios
account_collection = database.accounts
position_collection = database.positions
transaction_collection = database.transactions