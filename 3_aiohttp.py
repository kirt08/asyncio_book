import time
import asyncio
import aiohttp
from aiohttp import ClientSession

from functools import wraps

def async_timed(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        duration = time.perf_counter() - start
        print("Время выполенния: ", duration)
        return result
    return wrapper


@async_timed
async def fetch_status(url: str, session: ClientSession):
    async with session.get(url) as result:
        return result.status
    

@async_timed
async def main():
    async with ClientSession() as session:
        url = "https://google.com"
        status = await fetch_status(url, session)
        print(f"Status of resource: {url} is {status}")

asyncio.run(main())
