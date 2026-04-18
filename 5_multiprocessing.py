from asyncio import AbstractEventLoop
import asyncio
from functools import partial
import time
from concurrent.futures import ProcessPoolExecutor


def count(count_to: int) -> int:
    start = time.perf_counter()
    counter = 0
    while counter < count_to:
        counter += 1
    duration = time.perf_counter() - start
    print("Время выполенения: ", duration)
    return counter


async def main():
    with ProcessPoolExecutor() as process_pool:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        nums = [100_000_000, 1, 2, 5, 22, 100_000_000]
        calls: list[partial[int]] = [partial(count, num) for num in nums]
        calls_coros = []

        for call in calls:
            calls_coros.append(loop.run_in_executor(process_pool, call))

        results = await asyncio.gather(*calls_coros)

        for res in results:
            print(res)

if __name__ == "__main__":
    asyncio.run(main())

