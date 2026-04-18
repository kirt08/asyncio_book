import asyncio
from multiprocessing import Value
from concurrent.futures import ProcessPoolExecutor

shared_count = Value("d", 0)

def init(counter):
    global shared_count
    shared_count = counter

def increment():
    with shared_count.get_lock():
        shared_count.value += 1

async def main():
    counter = Value("d", 0)
    with ProcessPoolExecutor(initializer=init, initargs=(counter, )) as pool:
        await asyncio.get_running_loop().run_in_executor(pool, increment)
        print(counter.value)


if __name__ == "__main__":
    asyncio.run(main())

