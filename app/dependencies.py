from typing import Optional
from fastapi import Cookie
from fastapi import HTTPException


async def read_tables(access_token: Optional[str] = Cookie(None)):
    if access_token == None:
        raise HTTPException(status_code=400, detail="not signed in")

      