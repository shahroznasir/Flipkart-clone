from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
import os

# DB
from app.database import db_instance, Base

# Core
from app.core.auth_middleware import AuthMiddleware
from app.core.http_client import http_client
from app.core.logging_middleware import LoggingMiddleware
from app.core.exceptions import ExternalServiceError, BadRequestError

# Routers
from app.routers.auth_router import router as auth_router
from app.routers.product_router import router as product_router
from app.routers.user_router import router as user_router
from app.routers.cart_router import router as cart_router
from app.routers.order_router import router as order_router
from app.routers.payment_router import router as payment_router

# Rate Limiting
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware


# 🔁 Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Flipkart Clone API")

    if os.getenv("PYTEST_RUNNING") != "1":
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=db_instance.engine)

    logger.info("HTTP client initialized")

    yield

    logger.info("Shutting down Flipkart Clone API")

    await http_client.close()
    logger.info("HTTP client closed")

    db_instance.engine.dispose()
    logger.info("Database connection closed")


# 🚀 App Init (MUST come before limiter)
app = FastAPI(
    title="Flipkart Clone API",
    version="1.0.0",
    description="Flipkart Clone Backend with Clean Architecture",
    lifespan=lifespan
)


# 🔥 Rate Limiter (CORRECT placement)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


# 🧾 Logging Middleware
app.add_middleware(LoggingMiddleware)


# 🌐 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 🔐 Auth Middleware
app.add_middleware(AuthMiddleware)


# ❗ Exception Handlers
@app.exception_handler(ExternalServiceError)
async def external_service_handler(request: Request, exc: ExternalServiceError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.message}
    )


@app.exception_handler(BadRequestError)
async def bad_request_handler(request: Request, exc: BadRequestError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.message}
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal Server Error"}
    )


# 🔐 Swagger JWT Setup
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


# 📦 Routers
API_PREFIX = "/api/v1"

app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(user_router, prefix=API_PREFIX)
app.include_router(product_router, prefix=API_PREFIX)
app.include_router(cart_router, prefix=API_PREFIX)
app.include_router(order_router, prefix=API_PREFIX)
app.include_router(payment_router, prefix=API_PREFIX)


# 🏠 Root
@app.get("/", tags=["Root"])
@limiter.limit("5/minute")
def root(request: Request):
    return {
        "success": True,
        "message": "Flipkart Clone API Running",
        "docs": "/docs",
        "version": app.version
    }