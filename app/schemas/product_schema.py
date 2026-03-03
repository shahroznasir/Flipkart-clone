from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


# Base Schema (Shared Fields)

class ProductBase(BaseModel):

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Product name (3–100 characters)"
    )
    price: float = Field(
        ...,
        gt=0,
        description="Price must be greater than 0"
    )
    stock: int = Field(
        ...,
        ge=0,
        description="Stock cannot be negative"
    )

# Create Schema (Request)

class ProductCreate(ProductBase):
    pass

# Update Schema

class ProductUpdate(BaseModel):

    name: Optional[str] = Field(
        None,
        min_length=3,
        max_length=100
    )
    price: Optional[float] = Field(
        None,
        gt=0
    )
    stock: Optional[int] = Field(
        None,
        ge=0
    )

# Response Schema

class ProductResponse(ProductBase):

    id: int
    seller_id: int
    model_config = ConfigDict(
        from_attributes=True
    )