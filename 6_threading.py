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


