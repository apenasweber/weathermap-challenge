import logging
import os

from pymongo import MongoClient

from app.core.config import settings

logger = logging.getLogger(__name__)


class MongoDB:
    _client = None

    @classmethod
    def initialize(cls):
        cls._client = MongoClient(
            settings.MONGO_URL,
            username=settings.DB_USER,
            password=settings.DB_PASSWORD,
            authSource=settings.MONGO_DB_NAME,
            authMechanism="SCRAM-SHA-256",
        )
        logger.info("MongoDB client initialized")

    @classmethod
    def get_database(cls):
        if cls._client is None:
            raise Exception("MongoDB client is not initialized")
        return cls._client[settings.MONGO_DB_NAME]

    @classmethod
    def close(cls):
        if cls._client:
            cls._client.close()
            cls._client = None
            logger.info("MongoDB client closed")
