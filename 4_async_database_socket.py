from functools import wraps
import time

import asyncpg
import asyncio

from sql_commands import *


query = "INSERT INTO test_table (test_val) VALUES (52)";

def async_timed(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        duration = time.perf_counter() - start
        print("Время выполенния: ", duration)
        return result
    return wrapper


async def query_product(pool):
    async with pool.acquire() as connection:
        return await connection.fetch(query)

@async_timed
async def main():
    async with asyncpg.create_pool(
                        host = "0.0.0.0",
                        port = 5432,
                        user = "asyncio_book_user",
                        database = "asyncio_book",
                        password = "12345678",
                        min_size=6,
                        max_size=6
                    ) as pool:
        
        fetches = [await query_product(pool) for _ in range(10000)]
        # fetches = [query_product(pool) for _ in range(10000)]
        # await asyncio.gather(*fetches)
    

asyncio.run(main())

# 0.10414658800436882