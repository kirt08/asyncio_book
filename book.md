### asyncio.gather
**Время выполнение**: max(time(cor1), time(cor2), time(cor3))
**Главный недостаток**: Мы ждем выполение всех запросов даже если у нас 2 запроса выполня.тся 1 секунду, а третий 100 секунд.

*return_exception*: bool -> gather вернет список из результатов выполнения сопрограмм, если указать этот аргумент False, исключения будут возбуждаться, в случае True, исключения будут хранится в списке и мы можем наткнуться на него при итерации, поэтому можно использовать, например, isinstance(exception)


### asyncio.as_completed
**Главный плюс**: решает проблему gather -> можем обрабатывать результаты по мере выполнения таски, однако платим за это хаотичным порядком возврата, мы не знаем результат от какой таски нам пришел, можно использвоать только когда порядок НЕ важен!


### asyncio.wait
**Время выполнения** может варироваться от установленного значения в параметр *return_when*

Такая функция позволяет очень хорошо контрилорать происходящие процессы и писать логику самостоятельно. 
```python
@async_timed
async def fetch_status(url: str, session: ClientSession, delay: int):
    await asyncio.sleep(delay)
    async with session.get(url) as response:
        return response.status


async def main():
    async with ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(url, session, 1)),
            asyncio.create_task(fetch_status(url, session, 2)),
            asyncio.create_task(fetch_status("bad://ptyhon", session, 2)),
            asyncio.create_task(fetch_status(url, session, 3)),
        ]

        done, pending = await asyncio.wait(fetchers, return_when=asyncio.FIRST_EXCEPTION)

        for done_task in done:
            if done_task.exception() is None:
                print(done_task.result())
            else:
                print("Exception was found")

        for pending_task in pending:
            pending_task.cancel()

asyncio.run(main())
```

Допустим вот такой вариант с *return_when=asyncio.FIRST_COMPLETED*
```python
async def main():
    async with ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(url, session, 1)),
            asyncio.create_task(fetch_status(url, session, 2)),
            asyncio.create_task(fetch_status(url, session, 2)),
        ]

        done, pending = await asyncio.wait(fetchers, return_when=asyncio.FIRST_COMPLETED)

        print("Number of done tasks: ", len(done))
        print("Number of pending tasks: ", len(pending))

        for done_task in done:
            print(await done_task)
```

Пример создания потока и передачи в него функции:
```python
thread = Thread(target = echo, args = (connection, ))
thread.start()
```

Использование таких потоков в IO задачах практически эквивалентно ассинхронному подходу (в книге мы написали эхо-сервер на сокетах в двух вариация), однако при завершении главного потока через **CTRL + C** (возбуждение KeyboardInterrupt) дочерние потоки не будут уведомлены и продолжать работать (в нашем случае получать и отправлять данные). В книге представлено два варианта решения данной проблемы:

1. Использование потоков-демонов ("демоны" - специальный вид потоков предназначенный для выполнения длительных фоновых задач), такие потоки прекратят работу, когда родительский (главный поток Python) завершит работы (в нашем случае возбудит исключение KeyboardInterrupt).
Чтобы сделать из обычного потока -> поток-демон нужно добавить вызов одного метода:
```python
thread = Thread(target = echo, args = (connection, ))
thread.daemon = True
thread.start()
```
У данного подхода есть один существенный недостаток - такие потоки умирают без всякого уведомления.

2. Переопределение метода **run** внутри *Tread*
```python
from threading import Thread
import socket


class ClientThread(Thread):
    def __init__(self, client: socket.socket):
        super().__init__()
        self.client = client
    
    def run(self):
        try:
            while True:
                data = self.client.recv(2048)
                if not data:
                    raise BrokenPipeError("Connection closed!")
                print(f"Получено сообщение: {data}. Отправляю...")
                self.client.sendall(data)

        except OSError as e:
            print(f"Возбудилось исключение -> {e}. Останавливаем поток")

    def close(self):
        if self.is_alive():
            self.client.sendall(bytes("Подключение прервано", encoding="utf-8"))
            self.client.shutdown(socket.SHUT_RDWR)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 8000))
    server.listen()
    connection_threads = []
    try:
        while True:
            connection, addr = server.accept()
            thread = ClientThread(connection)
            connection_threads.append(thread)
            thread.start()
    except KeyboardInterrupt:
        print("Останавливаюсь")
        [thread.close() for thread in connection_threads]
```
Вроде бы в этом коде все достаточно тривиально и не требует никаких комментариев ( в ином случае загляните в CHATGPT -_- )