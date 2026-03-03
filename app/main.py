from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
import os

from app.database import db_instance, Base
from app.core.auth_middleware import AuthMiddleware
from app.routers.auth_router import router as auth_router
from app.routers.product_router import router as product_router
from app.routers.user_router import router as user_router
from app.routers.cart_router import router as cart_router
from app.routers.order_router import router as order_router
from app.routers.payment_router import router as payment_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Flipkart Clone API")

    # 🔹 DO NOT recreate tables during pytest
    if os.getenv("PYTEST_RUNNING") != "1":
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=db_instance.engine)

    yield

    logger.info("Shutting down Flipkart Clone API")
    db_instance.engine.dispose()
    logger.info("Database connection closed")


app = FastAPI(
    title="Flipkart Clone API",
    version="1.0.0",
    description="Flipkart Clone Backend with Clean Architecture",
    lifespan=lifespan
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    components = openapi_schema.setdefault("components", {})
    security_schemes = components.setdefault("securitySchemes", {})

    security_schemes["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }

    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthMiddleware)

API_PREFIX = "/api/v1"

app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(user_router, prefix=API_PREFIX)
app.include_router(product_router, prefix=API_PREFIX)
app.include_router(cart_router, prefix=API_PREFIX)
app.include_router(order_router, prefix=API_PREFIX)
app.include_router(payment_router, prefix=API_PREFIX)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Flipkart Clone API Running",
        "docs": "/docs",
        "version": app.version
    }