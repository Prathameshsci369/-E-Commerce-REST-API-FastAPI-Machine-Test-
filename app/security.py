

from fastapi import HTTPException, status, Depends
from fastapi.security import APIKeyHeader

# --- THROTTLING SETUP ---
from slowapi import Limiter
from slowapi.util import get_remote_address

# Create the limiter. It identifies users by IP address.
limiter = Limiter(key_func=get_remote_address)

# --- SECURITY SETUP ---
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != "12345":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )
    return api_key