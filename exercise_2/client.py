import time
from threading import Thread
import psutil

import requests


def main(server_type='sync'):
    # массив путей к папкам в которых будут анализироваться файлы
    # необходимо поменять их на существующие на том компьютере на котором будет происходить
    # запуск программы чтобы избежать ошибок
    dir_names = ["C:/Users",
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

    for i in range(400):
        t = Thread(target=req, args=(dir_names[1],))
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f'Сервер типа {server_type} обработал {n} запросов')


if __name__ == '__main__':
    server_type_variable = "threading"  # переменная для определения типа сервера(async или threading)
    process = psutil.Process().memory_info().rss / 1024 / 1024
    begin = time.time()
    main(server_type=server_type_variable)
    end = time.time() - begin
    mem = (psutil.Process().memory_info().rss / 1024 / 1024) - process
    print(f"Употреблённая память до: {mem} Mбайт")
    print(f"Время: {end} секунд")
    print(f"{server_type_variable} завершил работу\n\n")
