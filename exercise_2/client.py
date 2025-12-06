import time
from threading import Thread
import psutil

import requests


def main(server_type='sync'):
    dir_names = [ "C:/Users",
        "C:/Users/user/PycharmProjects/system-programming-test/exercise_1"]
    threads = []
    n = 0

    def req(dir_name):
        nonlocal n
        match server_type:
            case 'async':
                port = 8080
            case 'threading':
                port = 8081
        response = requests.get(f"http://127.0.0.1:{port}/?dir_name={dir_name}")
        print(f"Суммарное количество строк в файлах директории {dir_name} равна {response.text}")
        n += 1
        return n

    for i in dir_names:
        t = Thread(target=req, args=(i,))
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f'Сервер типа {server_type} обработал {n} запросов')


if __name__ == '__main__':
    server_type = "async"
    process_async = psutil.Process().memory_info().rss / 1024 / 1024
    begin = time.time()
    main(server_type=server_type)
    async_end = time.time() - begin
    mem_1 = (psutil.Process().memory_info().rss / 1024 / 1024) - process_async
    print(f"Употреблённая память до: {mem_1} Mбайт")
    print(f"Время: {async_end} секунд")
    print(f"{server_type} завершил работу\n\n")

