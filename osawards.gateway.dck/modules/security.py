# General imports
import hashlib
import json
import os
import secrets

# Model imports
from model.invalid_api_key_exception_model import InvalidApiKeyException

# FastAPI imports
from fastapi import Header # type: ignore


# Function: Hash an API Key
def hash_key(key: str) -> str:
    """Hash an API Key.

    Args:
        key (str): The unhashed key.
    
    Returns:
        str

    """

    return hashlib.sha256(key.encode()).hexdigest()


# Function: Verify an API Key
def verify_api_key(x_osawards_api_key: str = Header(...)) -> bool:
    """Verify an API Key.

    Args:
        x_osawards_api_key (str): The unhashed key.
    
    Returns:
        bool

    """
    
    key_hashed = os.getenv("GATEWAY_API_KEY_HASHED")
    received_key = hash_key(x_osawards_api_key)
    if key_hashed != received_key:
        raise InvalidApiKeyException
    return True
