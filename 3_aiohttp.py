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
            asyncio.create_task(fetch_status("bad://ptyhon", session, 2)),
            asyncio.create_task(fetch_status(url, session, 3)),
        ]

        done, pending = await asyncio.wait(fetchers, return_when=asyncio.FIRST_EXCEPTION)

        for done_task in done:
            if done_task.exception() is None:
                print(done_task.result())
            else:
                print("Exception was found")

        for pending_task in pending:
            pending_task.cancel()

asyncio.run(main())