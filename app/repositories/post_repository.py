from app.core.http_client import http_client
from app.utils.retry import retry

class PostRepository:
    async def get_posts(self):
        return await retry(lambda: http_client.get("/posts"))
    async def create_post(self, payload: dict):
        return await retry(lambda: http_client.post("/posts", json=payload))