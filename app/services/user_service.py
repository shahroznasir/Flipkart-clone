from fastapi import HTTPException, status

from app.entities.user_entity import UserEntity
from app.repositories.user_repository import UserRepository
from app.utils.security import hash_password


def create_user(db, user_request):
    repo = UserRepository()

    # Check existing user
    existing = repo.find_by_email(db, user_request.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )

    # Create user
    user = UserEntity(
        email=user_request.email,
        password=hash_password(user_request.password),
        role=user_request.role
    )

    repo.save(db, user)

    # Response
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role
    }
