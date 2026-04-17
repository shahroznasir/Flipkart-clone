import time
import uuid
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()

        logger.bind(request_id=request_id).info(
            f"Incoming request {request.method} {request.url}"
        )

        response = await call_next(request)

        duration = round(time.time() - start_time, 3)

        logger.bind(request_id=request_id).info(
            f"Completed {response.status_code} in {duration}s"
        )

        response.headers["X-Request-ID"] = request_id
        return response