from fastapi import APIRouter, Depends
from loguru import logger
from app.schemas.user_request import UserRequest
from app.services.user_service import UserService
from app.dependency import get_user_service


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    include_in_schema=False
)


# SAVE USER

@router.post("/")
def save_user(

    req: UserRequest,
    service: UserService = Depends(get_user_service)
):
    logger.info(f"Creating new user with email={req.email}")
    user = service.create_user(
        name=req.name,
        email=req.email,
        password=req.password
    )
    logger.success(f"User created successfully user_id={user.id}")
    return user


# GET ALL USERS

@router.get("/")
def get_users(
    service: UserService = Depends(get_user_service)
):
    logger.info("Fetching all users")
    users = service.get_all_users()
    logger.info(f"{len(users)} users fetched")
    return users