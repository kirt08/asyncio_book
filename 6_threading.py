import time
import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"Время выполнения функции {func.__name__} составило {duration} с")
        return res
    return wrapper

def get_status(url: str) -> int:
    response = requests.get(url)
    return response.status_code


@timer
def main():
    with ThreadPoolExecutor() as pool:
        urls = ["https://www.google.com" for _ in range(100)]
        results = pool.map(get_status, urls)
        for result in results:
            print(result)

main()