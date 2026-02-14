from app.entities.user_entity import UserEntity
from app.schemas.user_request import UserRequest
from app.schemas.user_response import UserResponse


def request_to_entity(req: UserRequest) -> UserEntity:
    return UserEntity(
        email=req.email,
        password=req.password
    )


def entity_to_response(entity: UserEntity) -> UserResponse:
    return UserResponse(
        id=entity.id,
        email=entity.email,
        role=entity.role
    )
