import time
from multiprocessing import Process


def timer(func: callable):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"Функция {func.__name__}: Время выполнения: ", duration)
        return result
    return wrapper


@timer
def count(count_to: int) -> int:
    counter = 0
    while counter < count_to:
        counter += 1
    return counter


@timer
def main():
    count_1 = Process(target = count, args=(100000000, ))
    count_2 = Process(target = count, args=(200000000, ))

    count_1.start() # сразу возвращает управление и начинает выполнять процесс
    count_2.start()

    count_1.join() # ждать завершение процесса. Метод блокирует выполнение пока процесс не завершится
    count_2.join()


if __name__ == "__main__":
    main()

