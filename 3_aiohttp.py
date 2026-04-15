import time
import asyncio
import aiohttp
from aiohttp import ClientSession

from functools import wraps

url = "https://www.google.com"

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
async def fetch_status(url: str, session: ClientSession, delay: int):
    await asyncio.sleep(delay)
    async with session.get(url) as response:
        return response.status


async def main():
    async with ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(url, session, 1)),
            asyncio.create_task(fetch_status(url, session, 2)),
            asyncio.create_task(fetch_status(url, session, 2)),
        ]

        done, pending = await asyncio.wait(fetchers, return_when=asyncio.FIRST_COMPLETED)

        print("Number of done tasks: ", len(done))
        print("Number of pending tasks: ", len(pending))

        for done_task in done:
            print(await done_task)

asyncio.run(main())