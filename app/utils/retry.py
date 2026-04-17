import asyncio

async def retry(func, retries=3, base_delay=0.5):
    for attempt in range(retries):
        try:
            return await func()
        except Exception:
            if attempt == retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            await asyncio.sleep(delay)