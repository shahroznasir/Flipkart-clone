from datetime import datetime, timedelta
from jose import jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user_request import UserRequest
from app.schemas.login_request import LoginRequest
from app.repositories.user_repository import UserRepository
from app.services.user_service import create_user
from app.utils.security import verify_password


SECRET_KEY = "super-secret-key-change-this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


class AuthService:

    @staticmethod
    def register_user(db: Session, user: UserRequest):
        return create_user(db, user)

    @staticmethod
    def login_user(db: Session, data: LoginRequest):
        repo = UserRepository()
        user = repo.find_by_email(db, data.email)

        if not user or not verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        payload = {
            "sub": str(user.id),
            "role": user.role,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            "access_token": token,
            "token_type": "bearer"
        }
