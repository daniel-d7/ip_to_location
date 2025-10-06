"""
IP processing utilities and functions.
"""

import ipaddress
from typing import List, Generator


def ip_to_score(ip: str) -> int:
    """
    Convert IP address to numeric score for sorting/comparison.
    
    Args:
        ip: IP address as string
        
    Returns:
        Numeric representation of IP address
    """
    ip_obj = ipaddress.ip_address(ip)
    return int(ip_obj)  # Returns 32-bit int for IPv4, 128-bit int for IPv6


def batch_ips(ip_list: List[str], batch_size: int) -> Generator[List[str], None, None]:
    """
    Split IP list into batches for processing.
    
    Args:
        ip_list: List of IP addresses
        batch_size: Size of each batch
        
    Yields:
        Batches of IP addresses
    """
    for i in range(0, len(ip_list), batch_size):
        yield ip_list[i : i + batch_size]