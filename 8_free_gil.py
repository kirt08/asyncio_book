import hashlib
import os
import string
import random
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Any, Coroutine
from functools import partial, wraps


def async_timer[R, **P](
    func: Callable[P, Coroutine[Any, Any, R]]
) -> Callable[P, Coroutine[Any, Any, R]]:
    
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        try:
            return await func(*args, **kwargs)
        finally:
            duration = time.perf_counter() - start
            print("duration: ", duration)

    return wrapper


def get_random_password(length: int) -> bytes:
    letters = string.ascii_letters.encode()
    return b"".join(bytes(random.choice(letters)) for _ in range(length))


def hash(password: bytes) -> str:
    salt = os.urandom(16)
    return hashlib.scrypt(
        password = password,
        salt = salt,
        n = 2048,
        p = 1,
        r = 8 
    )

@async_timer
async def main():
    with ThreadPoolExecutor() as pool:
        loop = asyncio.get_running_loop()
        passwords = [get_random_password(10) for _ in range(10_000)]
        tasks = [
            loop.run_in_executor(
                executor=pool,
                func = partial(hash, password),
            )
            for password in passwords
        ]
        await asyncio.gather(*tasks)


asyncio.run(main())

        