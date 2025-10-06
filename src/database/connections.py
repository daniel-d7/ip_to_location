"""
Database connection management for MongoDB and Redis.
"""

import pymongo
import redis
from .config import (
    MONGODB_URI, MONGODB_DATABASE, 
    REDIS_HOST, REDIS_PORT, REDIS_DB
)


class DatabaseConnections:
    """Manages database connections for MongoDB and Redis."""
    
    def __init__(self):
        self._mongo_client = None
        self._redis_client = None
        self._db = None
        
    @property
    def mongo_client(self):
        """Get MongoDB client instance."""
        if self._mongo_client is None:
            self._mongo_client = pymongo.MongoClient(MONGODB_URI)
        return self._mongo_client
    
    @property
    def database(self):
        """Get MongoDB database instance."""
        if self._db is None:
            self._db = self.mongo_client[MONGODB_DATABASE]
        return self._db
    
    @property
    def glamira_collection(self):
        """Get glamira collection from MongoDB."""
        from .config import MONGODB_GLAMIRA_COLLECTION
        return self.database[MONGODB_GLAMIRA_COLLECTION]
    
    @property
    def location_collection(self):
        """Get location collection from MongoDB."""
        from .config import MONGODB_LOCATION_COLLECTION
        return self.database[MONGODB_LOCATION_COLLECTION]
    
    @property
    def redis_client(self):
        """Get Redis client instance."""
        if self._redis_client is None:
            self._redis_client = redis.StrictRedis(
                host=REDIS_HOST, 
                port=REDIS_PORT, 
                db=REDIS_DB
            )
        return self._redis_client
    
    def close_connections(self):
        """Close all database connections."""
        if self._mongo_client:
            self._mongo_client.close()
        if self._redis_client:
            self._redis_client.close()


# Global database connections instance
db_connections = DatabaseConnections()