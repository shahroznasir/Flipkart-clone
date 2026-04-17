from fastapi import APIRouter
from app.services.post_service import PostService
from app.schemas.post_schema import PostRequest
from app.core.response import success_response
from slowapi.util import get_remote_address
from fastapi import Request

@router.get("/")
@limiter.limit("10/minute")
async def get_posts(request: Request):
    data = await service.fetch_posts()
    return success_response(data)

router = APIRouter(prefix="/posts", tags=["Posts"])
service = PostService()
@router.get("/")
async def get_posts():
    data = await service.fetch_posts()
    return success_response(data, "Posts fetched successfully")
@router.post("/")
async def create_post(request: PostRequest):
    data = await service.create_post(request)
    return success_response(data, "Post created successfully")