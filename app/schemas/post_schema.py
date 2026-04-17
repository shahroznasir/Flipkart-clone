from pydantic import BaseModel

class PostRequest(BaseModel):
    title: str
    body: str
    userId: int
class PostResponse(BaseModel):
    id: int
    title: str
    body: str
    userId: int