# Импорт
import requests
from bs4 import BeautifulSoup
import re
import json
import csv


# # Объявление URL и HEADERS
# URL = 'https://www.olx.ua/dom-i-sad/mebel/mebel-dlya-gostinoy/'
# HEADERS = {
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Mobile Safari/537.36'
# }
# Переменная req, которая возвращает результат работы get библиотеки requests
# Первый параметр - URL, второй - HEADERS
# req = requests.get(URL, headers=HEADERS)
# Сохраняем результат в переменную src
# src = req.text
# print(src)

# Лучше сохранять полученные данные в файл, чтобы не отправлять каждый раз на сайт запросы, так как
# это может его перегрузить и мы получить бан либо ограничение по времени использования
FILENAME = 'Portfolio/parsing/parsing-first/index.html'
# with open(FILENAME, 'w', encoding='utf-8') as file:
#     file.write(src)

# with open(FILENAME, encoding='utf-8') as file:
#     s = file.read()

# Далее сохранённый файл передаём в переменную и создаём элемент bs4
# soup = BeautifulSoup(s, 'lxml')

# # Находим нужные нам элементы
# goods = soup.find_all(class_='css-1bbgabe')

# all_goods = {}

# Проганяем их через цикл
# for good in goods:
#     good_text = good.find(class_="css-cqgwae-Text eu5v0x0").text
#     good_href = "https://www.olx.ua" + good.get("href")
#     # print(f"{good_text}: {good_href}")
#     all_goods[good_text] = good_href


# # Сохранение в json (Сохранение с такими параметрами поможет сэкономить время на поиск в интернете)
# with open('Portfolio/parsing/parsing-first/all_goods.json', 'w') as file:
#     json.dump(all_goods, file, indent=4, ensure_ascii=False)

with open('Portfolio/parsing/parsing-first/all_goods.json') as file:
    all_goods_json = json.load(file)

count = 0
for good_name, good_href in all_goods_json.items():

    rep = ['_', "'", ' ', '  ', '.', ',']
    for item in rep:
        if item in good_name:
            good_name = good_name.replace(item, "-")

    # req = requests.get(url=good_href, headers=HEADERS)
    # src = req.text

    # with open(f'Portfolio/parsing/parsing-first/data/{count}.{good_name}.html', 'w', encoding='utf-8') as file:
    #     file.write(src)

    with open(f'Portfolio/parsing/parsing-first/data/{count}.{good_name}.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    GoodName = soup.find(class_="css-u3ox0y-Text eu5v0x0").text
    GoodPrice = soup.find(class_='css-okktvh-Text eu5v0x0').text

    with open(f'Portfolio/parsing/parsing-first/data/goods.csv', 'a', encoding='cp1251') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            (
                GoodName,
                GoodPrice,
            )
        )

    count += 1
