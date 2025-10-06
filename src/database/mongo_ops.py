"""
MongoDB operations for IP and location data management.
"""

from typing import List, Generator, Dict, Any
import pandas as pd

from .connections import db_connections
from .redis_ops import get_ip_location
from ..config import BATCH_SIZE_FETCH, BATCH_SIZE_PROCESS


def fetch_all_ips() -> Generator[List[str], None, None]:
    """
    Fetch all IP addresses from the semantic collection in batches.
    
    Yields:
        Batches of IP addresses
    """
    semantic_collection = db_connections.semantic_collection
    cursor = semantic_collection.find({}, {"ip": 1, "_id": 0})
    
    batch = []
    for doc in cursor:
        batch.append(doc["ip"])
        if len(batch) == BATCH_SIZE_FETCH:
            yield batch
            batch = []
    if batch:
        yield batch


def get_unique_ips() -> List[str]:
    """
    Fetch all IPs from MongoDB and return unique IPs.
    
    Returns:
        List of unique IP addresses
    """
    print("Fetching all IPs from MongoDB...")
    all_ips = []
    for ip_batch in fetch_all_ips():
        all_ips.extend(ip_batch)
    print(f"Fetched {len(all_ips)} IPs")

    # Drop duplicates
    print("Dropping duplicates...")
    df = pd.DataFrame(all_ips, columns=["ip"])
    df_unique = df.drop_duplicates().reset_index(drop=True)
    unique_ips = df_unique["ip"].tolist()
    print(f"Unique IPs count: {len(unique_ips)}")
    
    return unique_ips


def insert_location_batch(ip_batch: List[str]) -> None:
    """
    Process a batch of IPs and insert location data to MongoDB.
    
    Args:
        ip_batch: List of IP addresses to process
    """
    location_collection = db_connections.location_collection
    docs = []
    
    for ip in ip_batch:
        location_data = get_ip_location(ip)
        if location_data:
            docs.append(location_data)
    
    if docs:
        location_collection.insert_many(docs)
        print(f"Inserted batch of {len(docs)} documents.")