from pydantic import BaseModel, Field, ConfigDict
from typing import List


# ==============================
# Add to Cart
# ==============================
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


# ==============================
# Update Quantity
# ==============================
class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=0)


# ==============================
# Cart Item Response
# ==============================
class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)


# ==============================
# Cart Response
# ==============================
class CartResponse(BaseModel):
    cart_id: int
    items: List[CartItemResponse]
