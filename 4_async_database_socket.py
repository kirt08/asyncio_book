from functools import wraps
import time

import asyncpg
import asyncio

from sql_commands import *


query1 = "INSERT INTO test_table (test_id, test_val) VALUES (1, 52)";
query2 = "INSERT INTO test_table (test_id, test_val) VALUES (2, 92)";

def async_timed(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        duration = time.perf_counter() - start
        print("Время выполенния: ", duration)
        return result
    return wrapper


# async def query_product(pool):
#     async with pool.acquire() as connection:
#         return await connection.fetch(query)

@async_timed
async def main():
    connection = await asyncpg.connect(
        host = "0.0.0.0",
        port = 5432,
        user = "asyncio_book_user",
        database = "asyncio_book",
        password = "12345678",
    )
    
    async with connection.transaction():
        await connection.execute(query1)
        await connection.execute(query2)

    query = "SELECT test_id, test_val FROM test_table;"
    res = await connection.fetch(query)
    print(res)

    await connection.close()

asyncio.run(main())
