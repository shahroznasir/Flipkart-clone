import os
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException, status
from app.core.security import verify_token

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        # BYPASS AUTH FOR TESTING
        if os.getenv("TESTING") == "true":
            request.state.user = {
                "user_id": 1,
                "role": "user"
            }
            return await call_next(request)

        # PUBLIC ROUTES
        public_paths = [
            "/",
            "/docs",
            "/openapi.json",
            "/api/v1/auth/login",
            "/api/v1/auth/register"
        ]
        if request.url.path in public_paths:
            return await call_next(request)

        # PROTECTED ROUTES
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing"
            )
        try:
            token = auth_header.split(" ")[1]
            payload = verify_token(token)
            request.state.user = {
                "user_id": payload["user_id"],
                "role": payload["role"]
            }
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return await call_next(request)