from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.product_service import ProductService


# REPOSITORIES

def get_user_repository(
    db: Session = Depends(get_db)
) -> UserRepository:
    return UserRepository(db)



def get_product_repository(
    db: Session = Depends(get_db)
) -> ProductRepository:
    return ProductRepository(db)


# SERVICES


def get_user_service(
    repo: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(repo)

def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    user_service: UserService = Depends(get_user_service)
) -> AuthService:
    return AuthService(user_service, user_repo)

def get_product_service(
    repo: ProductRepository = Depends(get_product_repository)
) -> ProductService:
    return ProductService(repo)


# AUTHENTICATION

def get_current_user(
    request: Request
) -> dict:
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return user


# AUTHORIZATION

def require_roles(
    roles: List[str]
):
    def checker(
        user: dict = Depends(get_current_user)
    ):
        if user["role"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )
        return user
    return checker