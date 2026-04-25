import asyncio
from asyncio import Transport, Future, AbstractEventLoop


class HTTPGetClientProtocol(asyncio.Protocol):
    def __init__(self, host: str, loop: AbstractEventLoop):
        self._host = host
        self._future: Future = loop.create_future()
        self._transport: Transport | None = None
        self._response_buffer: bytes = b""

    async def get_response(self):
        return await self._future
    
    def _get_request_bytes(self) -> bytes:
        request = f"GET / HTTP/1.1\r\n" \
                  f"Connection: close\r\n" \
                  f"Host: {self._host}\r\n\r\n"
        return request.encode()
    
    def connection_made(self, transport: Transport):
        print(f"Создано подключение к {self._host}")
        self._transport = transport
        self._transport.write(self._get_request_bytes())

    def data_received(self, data):
        print("Получены данные!")
        self._response_buffer = self._response_buffer + data

    def eof_received(self) -> bool | None:
        self._future.set_result(self._response_buffer.decode())
        return False
    
    def connection_lost(self, exc: Exception | None) -> None:
        if exc is None:
            print("одключение было закрыто без ошибок")
        else:
            self._future.set_exception(exc)

async def make_request(host: str, port: int, loop: AbstractEventLoop) -> str:
    def protocol_factory():
        return HTTPGetClientProtocol(host, loop)
    
    _, protocol = await loop.create_connection(protocol_factory, host=host, port=port)
    return await protocol.get_response()


async def main():
    loop: AbstractEventLoop = asyncio.get_running_loop()
    result = await make_request("www.google.com", 80, loop)
    print(result)

asyncio.run(main())