import logging
from typing import Optional

from fastapi import Depends
from app.core.config import settings
from app.services.kafka_service import KafkaService

logger = logging.getLogger(__name__)

# Global Kafka service instance
kafka_service: Optional[KafkaService] = None

async def connect_to_kafka() -> Optional[KafkaService]:
    """
    Initialize the Kafka service connection.

    If there's an error during connection, this function logs the error and returns None,
    allowing the application to continue functioning without Kafka.
    """
    global kafka_service

    if not settings.KAFKA_ENABLED:
        logger.info("Kafka is disabled. Skipping connection.")
        return None

    if kafka_service is None:
        try:
            logger.info(f"Connecting to Kafka at {settings.KAFKA_BOOTSTRAP_SERVERS}...")
            kafka_service = KafkaService(settings.KAFKA_BOOTSTRAP_SERVERS)
            await kafka_service.start()
            logger.info("Kafka connection established successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Kafka: {str(e)}")
            kafka_service = None
            return None

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

    If Kafka is disabled or if there's an error connecting to Kafka, this function
    returns None, allowing the application to continue functioning without Kafka.
    """
    if not settings.KAFKA_ENABLED:
        return None

    if kafka_service is None:
        try:
            await connect_to_kafka()
        except Exception as e:
            logger.error(f"Failed to connect to Kafka in get_kafka_service: {str(e)}")
            return None

    return kafka_service
