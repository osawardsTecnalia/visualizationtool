# General imports
import hashlib
import secrets


# Function: Generate an API Key
def generate_api_key() -> str:
    """Generate an API Key.

    Returns:
        str

    """

    return secrets.token_hex(32)  # 64 caracteres hex


# Function: Hash an API Key
def hash_api_key(key: str) -> str:
    """Hash an API Key.

    Args:
        key (str): The unhashed key.
    
    Returns:
        str

    """

    return hashlib.sha256(key.encode()).hexdigest()


# Funtion: Main
def main():
    
    print("---------------------------------")
    print("OSAwards API Key Generator v1.0.0")
    print("---------------------------------\n")
    api_key = generate_api_key()
    hashed_api_key = hash_api_key(api_key)
    print(f"         API Key  ->  {api_key}")
    print(f"  Hashed API Key  ->  {hashed_api_key}\n")


if __name__ == "__main__":
    main()