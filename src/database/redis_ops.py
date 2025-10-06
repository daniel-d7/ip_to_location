"""
Redis operations for IP2Location data management.
"""

import socket
import struct
from typing import Optional, Dict, Any

import IP2Location
from .connections import db_connections
from ..config import REDIS_DB_NAME, BIN_FILE_PATH, BATCH_SIZE_PROCESS, IP_STEP_SIZE
from ..processing.ip_processor import ip_to_score


def load_ip2location_bin_to_redis(bin_file_path: str = BIN_FILE_PATH) -> None:
    """
    Load IP2Location BIN data into Redis for fast lookups.
    
    Args:
        bin_file_path: Path to the IP2Location BIN file
    """
    print("Loading IP2Location BIN data into Redis...")

    db = IP2Location.IP2Location(bin_file_path)
    redis_client = db_connections.redis_client

    pipe = redis_client.pipeline()
    count = 0

    for ip_int in range(0, 4294967295, IP_STEP_SIZE):
        ip = socket.inet_ntoa(struct.pack("!L", ip_int))
        try:
            rec = db.get_all(ip)
            if rec:
                country = rec.country_short or ""
                region = rec.region or ""
                city = rec.city or ""
                val_str = f"{ip}|{country}|{region}|{city}"
                pipe.zadd(REDIS_DB_NAME, {val_str: ip_int})
                count += 1
                if count % BATCH_SIZE_PROCESS == 0:
                    pipe.execute()
                    print(f"Inserted {count} records into Redis...")
        except Exception as e:
            print(f"Error processing IP {ip}: {e}")
    
    if count % BATCH_SIZE_PROCESS != 0:
        pipe.execute()
        print(f"Inserted total {count} records into Redis...")

    print("Finished loading IP2Location BIN data into Redis.")


def get_ip_location(ip: str) -> Optional[Dict[str, Any]]:
    """
    Get location information for an IP address from Redis.
    
    Args:
        ip: IP address to lookup
        
    Returns:
        Dictionary with location information or None if not found
    """
    redis_client = db_connections.redis_client
    score = ip_to_score(ip)
    
    location = redis_client.zrevrangebyscore(
        REDIS_DB_NAME, score, 0, start=0, num=1
    )
    
    if location:
        location_str = location[0].decode("utf-8")
        location_fields = location_str.split("|")
        return {
            "ip": ip,
            "country": location_fields[1] if len(location_fields) > 1 else None,
            "region": location_fields[2] if len(location_fields) > 2 else None,
            "city": location_fields[3] if len(location_fields) > 3 else None,
        }
    
    return None