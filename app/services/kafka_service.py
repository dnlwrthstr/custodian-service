import json
import logging
from typing import Any, Dict, Optional

from aiokafka import AIOKafkaProducer
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class KafkaService:
    """
    Service for producing Kafka events.
    """
    def __init__(self, bootstrap_servers: str):
        """
        Initialize the Kafka producer service.
        
        Args:
            bootstrap_servers: Comma-separated list of Kafka broker addresses
        """
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        
    async def start(self):
        """
        Start the Kafka producer.
        """
        if self.producer is None:
            try:
                self.producer = AIOKafkaProducer(
                    bootstrap_servers=self.bootstrap_servers,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8')
                )
                await self.producer.start()
                logger.info(f"Kafka producer started with bootstrap servers: {self.bootstrap_servers}")
            except Exception as e:
                logger.error(f"Failed to start Kafka producer: {str(e)}")
                raise
    
    async def stop(self):
        """
        Stop the Kafka producer.
        """
        if self.producer is not None:
            try:
                await self.producer.stop()
                self.producer = None
                logger.info("Kafka producer stopped")
            except Exception as e:
                logger.error(f"Failed to stop Kafka producer: {str(e)}")
                raise
    
    async def produce_event(self, topic: str, data: Dict[str, Any], key: Optional[str] = None):
        """
        Produce a Kafka event.
        
        Args:
            topic: Kafka topic to produce to
            data: Event data to produce
            key: Optional key for the event
        """
        if self.producer is None:
            logger.error("Kafka producer not started")
            return
        
        try:
            key_bytes = key.encode('utf-8') if key else None
            await self.producer.send_and_wait(topic, data, key=key_bytes)
            logger.info(f"Produced event to topic {topic}: {data}")
        except Exception as e:
            logger.error(f"Failed to produce event to topic {topic}: {str(e)}")
            # Don't raise the exception to avoid breaking the main application flow
            # Just log the error