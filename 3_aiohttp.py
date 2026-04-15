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
            fetch_status(url, session, 1),
            fetch_status(url, session, 1),
            fetch_status(url, session, 10)
        ]

        for done_task in asyncio.as_completed(fetchers, timeout=2):
            try:
                res = await done_task
                print(res)
            except asyncio.TimeoutError:
                print("Timeout!!!")
            
        for task in asyncio.tasks.all_tasks():
            print(task)

asyncio.run(main())


