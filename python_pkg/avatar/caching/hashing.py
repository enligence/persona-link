"""
Hash methods that can be used to hash data.
"""

import hashlib
from typing import Any

def sha256hash(data: any) -> str:
    return hashlib.sha256(str(data).encode()).hexdigest()

def md5hash(data: any) -> str:
    return hashlib.md5(str(data).encode()).hexdigest()

