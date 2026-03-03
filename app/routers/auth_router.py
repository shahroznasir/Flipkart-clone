from fastapi import APIRouter, Depends, status

from app.schemas.user_request import UserRequest
from app.schemas.login_request import LoginRequest
from app.services.auth_service import AuthService
from app.dependency import get_auth_service
from loguru import logger

router = APIRouter(prefix="/auth", tags=["Auth"])

# Router (dependency injection)-> Service (Request) -> use mapper to convert/map request to entity -> send this mapper (entity)  -> Repository -> Database (session)
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    user: UserRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    logger.info("register api is called")
    return auth_service.register_user(user)

@router.post("/login")
def login(
    data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):

    return auth_service.login_user(data)
