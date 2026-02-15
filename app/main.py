from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import Base, engine
from app.routers.auth_router import router as auth_router
from app.routers.cart_router import router as cart_router
from app.routers.order_router import router as order_router
from app.routers.payment_router import router as payment_router
from app.routers.product_router import router as product_router
from app.routers.user_router import router as user_router


# ✅ Import ALL entities here so SQLAlchemy registers them

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
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(user_router)

# =====================
# ROOT CHECK
# =====================
@app.get("/")
def root():
    return {"status": "API is running"}
