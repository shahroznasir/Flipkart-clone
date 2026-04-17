from app.repositories.post_repository import PostRepository
from app.schemas.post_schema import PostRequest

class PostService:
    def __init__(self):
        self.repo = PostRepository()
    async def fetch_posts(self):
        return await self.repo.get_posts()
    async def create_post(self, request: PostRequest):
        return await self.repo.create_post(request.dict())