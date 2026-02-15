from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.deps import get_db
from app.schemas.user_request import UserRequest
from app.schemas.login_request import LoginRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRequest, db: Session = Depends(get_db)):
    return auth_service.register_user(db, user)


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return AuthService.login_user(db, data)
