import httpx
from app.core.config import settings
from app.core.exceptions import ExternalServiceError

class HTTPClient:
    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url=settings.BASE_URL,
            timeout=httpx.Timeout(5.0, connect=2.0),
            headers={
                "Authorization": f"Bearer {settings.API_TOKEN}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
    async def get(self, url: str, params: dict = None):
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise ExternalServiceError(
                message=f"External API error: {e.response.text}",
                status_code=e.response.status_code
            )
        except httpx.RequestError:
            raise ExternalServiceError("External service unavailable")

    async def post(self, url: str, json: dict = None):
        try:
            response = await self.client.post(url, json=json)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise ExternalServiceError(
                message=f"External API error: {e.response.text}",
                status_code=e.response.status_code
            )
        except httpx.RequestError:
            raise ExternalServiceError("External service unavailable")

    async def close(self):
        await self.client.aclose()

http_client = HTTPClient()