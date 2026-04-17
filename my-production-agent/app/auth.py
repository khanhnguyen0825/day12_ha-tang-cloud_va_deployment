from fastapi import Header, HTTPException, Depends
from .config import settings

async def verify_api_key(x_api_key: str = Header(...)):
    """
    Xác thực API Key từ Header.
    """
    if x_api_key != settings.AGENT_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API Key"
        )
    return "authorized_user"
