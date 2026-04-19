import time
import asyncio
import requests
from threading import Lock
from functools import partial
from concurrent.futures import ThreadPoolExecutor


counter_lock = Lock()
counter: int = 0


def timer(func):
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = await func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"Время выполнения функции {func.__name__} составило {duration} с")
        return res
    return wrapper

def get_status(url: str) -> int:
    global counter
    response = requests.get(url)
    with counter_lock:
        counter += 1
    return response.status_code

async def reporter(request_count: int):
    while counter < request_count:
        print(f"Завершено {counter}/{request_count}")
        await asyncio.sleep(.5)

@timer
async def main():
    requests_count = 200
    urls = ["https://www.google.com" for _ in range(requests_count)]

    reporter_task = asyncio.create_task(reporter(requests_count))
    tasks = [asyncio.to_thread(get_status, url) for url in urls]
    
    results = await asyncio.gather(*tasks)
    await reporter_task
    print(results)


if __name__ == "__main__":
    asyncio.run(main())