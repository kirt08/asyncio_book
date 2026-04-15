import asyncio
import socket


class AsyncContextManager:
    def __init__(self, server_socket):
        self._connection: socket.socket | None = None
        self._server_socket: socket.socket = server_socket

    async def __aenter__(self):
        print("Enter to context manager and waiting for connection...")
        loop = asyncio.get_event_loop()
        con, address = await loop.sock_accept(self._server_socket)
        self._connection = con
        print(f"Connection from {address} was accepted")
        return self._connection
    
    async def __aexit__(self, exc_type, exc, tb):
        print("Exit from context manager.")
        self._connection.close()
        print("Connection aborted")


async def main():
    loop = asyncio.get_event_loop()

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setblocking(False)
    server_socket.bind(("127.0.0.1", 8000))
    server_socket.listen()

    async with AsyncContextManager(server_socket) as connection:
        data = await loop.sock_recv(connection, 1024)
        print(data)

asyncio.run(main())