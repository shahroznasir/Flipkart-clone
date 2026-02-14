from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db
from app.schemas.user_request import UserRequest
from app.services.user_service import create_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
def save_user(req: UserRequest, db: Session = Depends(get_db)):
    return create_user(db, req)
