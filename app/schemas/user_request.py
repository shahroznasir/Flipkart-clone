from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Literal

class UserRequest(BaseModel):
    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=50,
        description="Password must be 8-50 characters"
    )

    role: Literal["admin", "seller", "user"] = "user"

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one number")
        return value
