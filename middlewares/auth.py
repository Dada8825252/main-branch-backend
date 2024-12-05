from fastapi import Request
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from schemas.user import UserProfile

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

async def auth_middleware(request: Request, call_next):
    token = request.headers.get("Authorization")
    if token is None:
        user = UserProfile(
            id = 2147483647,
            name = "anymous",
            role = "anymous",
            is_2fa_enabled = "false"
        )
    else:
        try:
            token = token.split('Bearer ')[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user = UserProfile(
                id = payload.get("id"),
                name = payload.get("name"),
                role = payload.get("role"),
                is_2fa_enabled = payload.get("is_2fa_enabled")
            )
        except JWTError:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})
    
    request.state.user = user
    return await call_next(request)