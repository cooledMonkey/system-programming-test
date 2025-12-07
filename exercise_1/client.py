import time
from threading import Thread
import psutil

import requests


def main(server_type='async'):
    # массив ссылок по которым будут парситься товары
    links = ["https://dental-first.ru/catalog/stomatologicheskie-materialy/plombirovochnye-materialy-shpritsy/shpritsy-estelite-/estelite-posterior/",
             "https://dental-first.ru/catalog/stomatologicheskie-materialy/plombirovochnye-materialy-shpritsy/shpritsy-estelite-/estelite-sigma-quick/",
             "https://dental-first.ru/catalog/stomatologicheskie-materialy/ekrany-i-ochki-zashchitnye/ochki-zashchitnye-clean-safe/",
             "https://dental-first.ru/catalog/stomatologicheskie-materialy/ekrany-i-ochki-zashchitnye/ekrany-i-ochki-zashchitnye-rossiya/",
             "https://dental-first.ru/catalog/stomatologicheskoe-oborudovanie/stomatologicheskie-nakonechniki-tekhnologiya/"]
    threads = []
    n = 0
    def req(link):
        nonlocal n
        match server_type:
            case 'async': port = 8080
            case 'threading': port = 8081
        response = requests.get(f"http://127.0.0.1:{port}/?url={link}")
        print(f"Суммарная стоимость всех товаров со страницы {link} равна {response.text}₽")
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
    server_type_choice = "threading"  # переменная для определения типа сервера(async или threading)
    ram_info = psutil.virtual_memory()
    process_async = psutil.Process().memory_info().rss/1024/1024
    begin = time.time()
    main(server_type=server_type_choice)
    async_end = time.time() - begin
    mem_1 = (psutil.Process().memory_info().rss / 1024 / 1024) - process_async
    print(f"Употреблённая память до: {mem_1} Mбайт")
    print(f"Время: {async_end} секунд")
    print(f"{server_type_choice} завершил работу\n\n")


