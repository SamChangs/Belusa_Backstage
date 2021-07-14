from fastapi import Cookie, Depends, status
from fastapi import HTTPException
from typing import Optional

async def auth_pages(access_token: Optional[str] = Cookie(None)):
    if access_token == None:
        return False

async def verify_key(access_token: Optional[str] = Cookie(None)):
    if access_token == None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    


