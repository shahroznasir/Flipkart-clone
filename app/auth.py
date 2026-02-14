from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta

from app.deps import get_db
from app.schemas.user_request import UserRequest
from app.schemas.login_request import LoginRequest
from app.services.user_service import create_user
from app.repositories.user_repository import UserRepository
from app.utils.security import verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])

# =====================
# JWT CONFIG
# =====================
SECRET_KEY = "super-secret-key-change-this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# =====================
# REGISTER
# =====================
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRequest, db: Session = Depends(get_db)):
    return create_user(db, user)


# =====================
# LOGIN (ONLY email + password)
# =====================
@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    repo = UserRepository()
    user = repo.find_by_email(db, data.email)   # ✅ FIXED HERE

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
