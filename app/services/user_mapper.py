from app.models import UserEntity
from app.schemas import UserRequest, UserResponse

def request_to_entity(req: UserRequest) -> UserEntity:
    return UserEntity(
        email=req.email,
        password=req.password
    )

def entity_to_response(entity: UserEntity) -> UserResponse:
    return UserResponse(
        id=entity.id,
        email=entity.email
    )
