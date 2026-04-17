from fastapi import HTTPException, status
from app.core.logger import logger
from app.schemas.login_request import LoginRequest
from app.schemas.user_request import UserRequest
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.core.security import create_access_token
from app.utils.security import verify_password


class AuthService:

    def __init__(
        self,
        user_service: UserService,
        user_repo: UserRepository
    ):
        self.user_service = user_service
        self.user_repo = user_repo


    def register_user(self, user: UserRequest):
        logger.info(
            "User registration attempt | email={}",
            user.email
        )

        created_user = self.user_service.create_user(user)

        logger.info(
            "User registered successfully | user_id={} email={}",
            created_user["id"],
            created_user["email"]
        )

        return created_user


    def login_user(self, data: LoginRequest):
        logger.info(
            "Login attempt | email={}",
            data.email
        )

        user = self.user_repo.find_by_email(data.email)

        if not user:
            logger.warning(
                "Login failed - user not found | email={}",
                data.email
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email"
            )

        if not verify_password(data.password, user.password):
            logger.warning(
                "Login failed - incorrect password | email={}",
                data.email
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password"
            )

        logger.info(
            "Login successful | user_id={} email={} role={}",
            user.id,
            user.email,
            user.role
        )

        token = create_access_token({
            "user_id": user.id,
            "email": user.email,
            "role": user.role
        })

        logger.debug(
            "Access token generated | user_id={}",
            user.id
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "idtg": user.id,
                "email": user.email,
                "role": user.role
            }
        }