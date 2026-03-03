from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas.user_request import UserRequest
from app.utils.security import hash_password
from app.core.logger import logger


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, user: UserRequest):
        logger.info(
            "User creation started | email={}",
            user.email
        )

        # Check existing
        existing = self.user_repo.find_by_email(user.email)
        if existing:
            logger.warning(
                "User creation failed - email already exists | email={}",
                user.email
            )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Convert to dict (Pydantic v2 safe)
        user_data = user.model_dump()

        # HASH PASSWORD (CRITICAL)
        user_data["password"] = hash_password(user.password)

        # Save user
        new_user = self.user_repo.create(user_data)

        logger.info(
            "User created successfully | user_id={} email={}",
            new_user.id,
            new_user.email
        )

        # Return response
        return {
            "id": new_user.id,
            "email": new_user.email,
            "role": new_user.role
        }