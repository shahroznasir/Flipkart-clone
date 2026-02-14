from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db import SessionLocal
from app.entities.user_entity import UserEntity



# =========================
# DATABASE DEPENDENCY
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# JWT CONFIG
# =========================
SECRET_KEY = "super-secret-key-change-this"
ALGORITHM = "HS256"

security = HTTPBearer()


# =========================
# GET CURRENT USER FROM TOKEN
# =========================
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid JWT token"
        )

    user = db.query(UserEntity).filter(UserEntity.id == user_id).first()


    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


# =========================
# ROLE-BASED AUTHORIZATION
# =========================
def require_roles(allowed_roles: list[str]):

    def role_checker(user = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return user

    return role_checker
