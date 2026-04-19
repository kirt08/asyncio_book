import time
import requests
import asyncio
from functools import partial


def timer(func):
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = await func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"Время выполнения функции {func.__name__} составило {duration} с")
        return res
    return wrapper

def get_status(url: str) -> int:
    response = requests.get(url)
    return response.status_code

@timer
async def main1():
    loop = asyncio.get_event_loop()
    urls = ["https://www.google.com" for _ in range(50)]
    tasks = [
        loop.run_in_executor(executor = None, func = partial(get_status, url))
        for url in urls
    ]
    results = await asyncio.gather(*tasks)
    print(results)

@timer
async def main2():
    urls = ["https://www.google.com" for _ in range(50)]
    tasks = [asyncio.to_thread(get_status, url) for url in urls]
    results = await asyncio.gather(*tasks)
    print(results)


if __name__ == "__main__":
    asyncio.run(main2())