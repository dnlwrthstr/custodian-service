import logging
from typing import Optional

from fastapi import Depends
from app.core.config import settings
from app.services.kafka_service import KafkaService

logger = logging.getLogger(__name__)

# Global Kafka service instance
kafka_service: Optional[KafkaService] = None

async def connect_to_kafka() -> KafkaService:
    """
    Initialize the Kafka service connection.
    """
    global kafka_service
    
    if not settings.KAFKA_ENABLED:
        logger.info("Kafka is disabled. Skipping connection.")
        return None
    
    if kafka_service is None:
        logger.info(f"Connecting to Kafka at {settings.KAFKA_BOOTSTRAP_SERVERS}...")
        kafka_service = KafkaService(settings.KAFKA_BOOTSTRAP_SERVERS)
        await kafka_service.start()
    
    return kafka_service

async def close_kafka_connection():
    """
    Close the Kafka service connection.
    """
    global kafka_service
    
    if kafka_service is not None:
        logger.info("Closing Kafka connection...")
        await kafka_service.stop()
        kafka_service = None

async def get_kafka_service() -> Optional[KafkaService]:
    """
    Get the Kafka service instance.
    
    This function is used as a FastAPI dependency to provide the Kafka service
    to API endpoints and other services.
    """
    if not settings.KAFKA_ENABLED:
        return None
        
    if kafka_service is None:
        await connect_to_kafka()
    
    return kafka_service