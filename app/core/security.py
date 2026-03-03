from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, status
import os

# CONFIG

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "super-secret-key-change-this"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# CREATE TOKEN

def create_access_token(
    data: dict
) -> str:

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})
    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token

# VERIFY TOKEN (USED BY MIDDLEWARE)

def verify_token(
    token: str
) -> dict:

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


# OPTIONAL: DECODE TOKEN (SAFE UTILITY)


def decode_access_token(
    token: str
):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        return None