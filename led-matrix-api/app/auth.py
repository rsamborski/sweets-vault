import os
from dotenv import load_dotenv
from fastapi import Header, HTTPException, status

load_dotenv()

API_KEY_NAME = "X-API-Key"
LED_API_KEY = os.getenv("LED_API_KEY")

async def get_api_key(x_api_key: str = Header(..., alias=API_KEY_NAME)):
    if not LED_API_KEY:
        # If no key is configured in env, we might want to fail safe or warn.
        # For this implementation, we'll assume it's required.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server configuration error: API Key not set",
        )
    
    if x_api_key != LED_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return x_api_key
