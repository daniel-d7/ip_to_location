# IP to Location Processor

A high-performance Python application that processes IP addresses from MongoDB and enriches them with geographic location data using IP2Location database. The system uses Redis for caching and batch processing for optimal performance.

## Features

- **Bulk IP Processing**: Processes large datasets of IP addresses from MongoDB
- **Geographic Enrichment**: Maps IP addresses to country, region, and city information
- **Redis Caching**: Uses Redis as a fast lookup cache for IP2Location data
- **Concurrent Processing**: Multi-threaded processing for improved performance
- **Duplicate Handling**: Automatically removes duplicate IP addresses
- **Batch Operations**: Efficient batch processing to handle large datasets

## Project Structure

```
ip_to_location/
├── main.py                    # Main entry point
├── README.md                  # Project documentation
└── src/                       # Source code directory
    ├── __init__.py
    ├── config.py              # Configuration settings
    ├── database/              # Database-related modules
    │   ├── __init__.py
    │   ├── connections.py     # Database connection management
    │   ├── mongo_ops.py       # MongoDB operations
    │   └── redis_ops.py       # Redis operations
    └── processing/            # Processing modules
        ├── __init__.py
        └── ip_processor.py    # IP processing utilities
```

## Architecture

```
MongoDB (semantic collection) → IP Extraction → Redis Cache Lookup → MongoDB (location collection)
```

1. **Data Source**: Fetches IP addresses from the `semantic` collection in MongoDB
2. **Caching Layer**: Uses Redis with sorted sets for fast IP range lookups
3. **Processing**: Multi-threaded batch processing with configurable workers
4. **Output**: Stores enriched location data in the `location` collection

## Prerequisites

- Python 3.7+
- MongoDB instance
- Redis server
- IP2Location BIN database file

## Dependencies

Install the required Python packages:

```bash
pip install pymongo redis pandas IP2Location
```

## Configuration

### Database Connections

The application uses a modular structure with centralized configuration management through `src/config.py` and connection management through `src/database/connections.py`.

### Configuration

Update the configuration in `src/config.py`:

```python
# Database Configuration
MONGODB_URI = "mongodb://username:password@localhost:27017/"
REDIS_HOST = "localhost"
REDIS_PORT = 6379

# IP2Location Configuration
BIN_FILE_PATH = "IP-COUNTRY-REGION-CITY.BIN"  # Update with your file path

# Performance Tuning
BATCH_SIZE_PROCESS = 10000  # Processing batch size
MAX_WORKERS = 5             # Number of concurrent threads
```

## Usage

1. **Prepare Data Sources**:
   - Ensure MongoDB is running with a `semantic` collection containing IP addresses
   - Have your IP2Location BIN file ready
   - Start Redis server

2. **Run the Application**:
   ```bash
   python main.py
   ```

## Data Flow

### Input Data Structure
The application expects IP addresses in the MongoDB `semantic` collection:
```json
{
  "ip": "192.168.1.1",
  "_id": "..."
}
```

### Output Data Structure
Enriched data is stored in the `location` collection:
```json
{
  "ip": "192.168.1.1",
  "country": "US",
  "region": "California",
  "city": "San Francisco"
}
```

## Performance Considerations

- **Memory Usage**: The application loads IP data into Redis for fast lookups
- **Batch Processing**: Processes IPs in configurable batches to balance memory and performance
- **Concurrency**: Uses ThreadPoolExecutor for parallel processing
- **Deduplication**: Removes duplicate IPs using pandas before processing

## Error Handling

- Individual IP processing errors are logged but don't stop the entire process
- Batch processing errors are caught and reported
- Invalid IP addresses are skipped automatically

## Monitoring

The application provides progress updates:
- Redis data loading progress
- IP fetching statistics
- Duplicate removal results
- Batch processing status

## Database Schema

### Collections Used

- **semantic**: Source collection containing IP addresses
- **location**: Target collection for enriched location data

### Redis Structure

- **Key**: `IP2LOCATION_DB`
- **Type**: Sorted Set (ZSET)
- **Score**: Numeric IP value for range queries
- **Value**: `IP|Country|Region|City` format

## Troubleshooting

### Common Issues

1. **Memory Issues**: Reduce `BATCH_SIZE_PROCESS` and `MAX_WORKERS`
2. **Connection Errors**: Verify MongoDB and Redis connection strings
3. **File Not Found**: Ensure IP2Location BIN file path is correct
4. **Performance**: Adjust batch sizes based on your system capabilities

### Logs

Monitor the console output for:
- Data loading progress
- Processing statistics
- Error messages
- Completion status

## License

This project is provided as-is for educational and development purposes.

## Contributing

Feel free to submit issues and pull requests to improve the application.