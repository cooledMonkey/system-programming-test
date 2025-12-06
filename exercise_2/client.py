import time
from threading import Thread
import psutil

import requests


def main(server_type='sync'):
    links = ["C:/Users",
             "C:/Users/user/PycharmProjects/system-programming-test/exercise_1"]
    threads = []
    n = 0

    def req(link):
        nonlocal n
        match server_type:
            case 'async':
                port = 8080
            case 'threading':
                port = 8081
        response = requests.get(f"http://127.0.0.1:{port}/?dir_name={link}")
        print(f"Суммарное количество строк в файлах директории {link} равна {response.text}")
        n += 1
        return n

    for i in range(len(links)):
        t = Thread(target=req, args=(links[i],))
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f'Сервер типа {server_type} обработал {n} запросов')


if __name__ == '__main__':
    ram_info = psutil.virtual_memory()
    process_async = psutil.Process().memory_info().rss / 1024 / 1024
    begin = time.time()
    main(server_type='async')
    async_end = time.time() - begin
    mem_1 = (psutil.Process().memory_info().rss / 1024 / 1024) - process_async
    print(f"Употреблённая память до: {mem_1} Mбайт")
    print(f"Время: {async_end} секунд")
    print("async завершил работу\n\n")

    ram_info2 = psutil.virtual_memory()
    process_threading = psutil.Process().memory_info().rss / 1024 / 1024
    begin = time.time()
    main(server_type='threading')
    mem_2 = (psutil.Process().memory_info().rss / 1024 / 1024) - process_threading
    threading_end = time.time() - begin
    print(f"Употреблённая память до: {mem_2} Mбайт")
    print(f"Время: {time.time() - begin} секунд")
    print("threading завершил работу\n\n")
