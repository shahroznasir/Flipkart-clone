from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import Base, engine
from app.auth import router as auth_router

from app.routers import products, cart, orders, payments

# ✅ Import ALL entities here so SQLAlchemy registers them
from app.entities.user_entity import UserEntity
from app.entities.product_entity import ProductEntity
from app.entities.cart_entity import CartEntity
from app.entities.order_entity import OrderEntity
from app.entities.order_item_entity import OrderItemEntity
from app.entities.payment_entity import PaymentEntity

# =====================
# APP INIT
# =====================
app = FastAPI(title="Flipkart Clone API")

# =====================
# CORS
# =====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================
# DATABASE TABLES
# =====================
Base.metadata.create_all(bind=engine)

# =====================
# ROUTERS
# =====================
app.include_router(auth_router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(payments.router)

# =====================
# ROOT CHECK
# =====================
@app.get("/")
def root():
    return {"status": "API is running"}
