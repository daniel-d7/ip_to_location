"""
Main entry point for the IP to Location processor.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed

from src.config import MAX_WORKERS, BIN_FILE_PATH
from src.database.redis_ops import load_ip2location_bin_to_redis
from src.database.mongo_ops import get_unique_ips, insert_location_batch
from src.database.connections import db_connections
from src.processing.ip_processor import batch_ips


def main():
    """Main processing function."""
    try:
        # Step 1: Load IP2Location BIN to Redis
        load_ip2location_bin_to_redis(BIN_FILE_PATH)

        # Step 2: Get unique IPs from MongoDB
        unique_ips = get_unique_ips()

        # Step 3: Process IPs concurrently
        print("Querying IP location and inserting to MongoDB...")
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = []
            for ip_batch in batch_ips(unique_ips):
                futures.append(executor.submit(insert_location_batch, ip_batch))
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error in batch processing: {e}")
                    
        print("Processing completed successfully!")
        
    except Exception as e:
        print(f"Error in main processing: {e}")
    finally:
        # Clean up connections
        db_connections.close_connections()


if __name__ == "__main__":
    main()
