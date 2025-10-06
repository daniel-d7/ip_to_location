"""
Configuration settings for the IP to Location processor.
"""

# Database Configuration
MONGODB_URI = "mongodb://daniel:Phieulang6868@localhost:27017/"
MONGODB_DATABASE = "public"
MONGODB_SEMANTIC_COLLECTION = "semantic"
MONGODB_LOCATION_COLLECTION = "location"

# Redis Configuration
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_DB_NAME = "IP2LOCATION_DB"

# IP2Location Configuration
BIN_FILE_PATH = "IP-COUNTRY-REGION-CITY.BIN"  # Change to your BIN file path

# Processing Configuration
BATCH_SIZE_PROCESS = 10000
BATCH_SIZE_FETCH = 1000000
MAX_WORKERS = 5
IP_STEP_SIZE = 100000  # Step size for IP range processing