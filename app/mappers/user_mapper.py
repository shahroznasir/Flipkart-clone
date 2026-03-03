from app.schemas.user_request import UserRequest
from app.entities.user_entity import UserEntity
from app.utils.security import hash_password


class UserMapper:

    @staticmethod
    def request_to_entity(user_request: UserRequest) -> dict:
        return {
            "email": user_request.email,
            "password": user_request.password,
            "role": getattr(user_request, "role", "user")

        }


    @staticmethod
    def entity_to_response(user_entity: UserEntity) -> dict:

        return {
            "id": user_entity.id,
            "email": user_entity.email,
            "role": user_entity.role
        }