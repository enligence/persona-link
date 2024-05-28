"""
Hash methods that can be used to hash data.
"""

import hashlib


def sha256hash(data: any) -> str:
    """
    Generate a SHA256 hash for the given data
    
    Parameters:
        data (any): The data to hash
        
    Returns:
        str: The SHA256 hash of the data
    """
    return hashlib.sha256(str(data).encode()).hexdigest()

def md5hash(data: any) -> str:
    """
    Generate an MD5 hash for the given data
    
    Parameters:
        data (any): The data to hash
        
    Returns:
        str: The MD5 hash of the data
    """
    return hashlib.md5(str(data).encode()).hexdigest()

