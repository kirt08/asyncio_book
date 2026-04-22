import hashlib
import os
import string
import random
import time


def get_random_password(length: int) -> bytes:
    letters = string.ascii_letters.encode()
    return b"".join(bytes(random.choice(letters)) for _ in range(length))

passwords = [get_random_password(10) for _ in range(10_000)]

def hash(password: bytes) -> str:
    salt = os.urandom(16)
    return hashlib.scrypt(
        password = password,
        salt = salt,
        n = 2048,
        p = 1,
        r = 8 
    )

start = time.time()

for password in passwords:
    hash(password)

end = time.time()
print(end - start)