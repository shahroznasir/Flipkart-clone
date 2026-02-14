from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app import entities as models, schemas, auth


def register_user(user: schemas.UserCreate, db: Session):
    try:
        new_user = models.User(
            email=user.email,
            password=auth.hash_pass(user.password),
            role=user.role
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "id": new_user.id,
            "email": new_user.email,
            "role": new_user.role
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def login_user(user: schemas.UserLogin, db: Session):
    existing_user = db.query(models.User).filter_by(
        email=user.email
    ).first()

    if not existing_user or not auth.verify(user.password, existing_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = auth.create_token(
        {"id": existing_user.id, "role": existing_user.role}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
