# -*- coding: utf8 -*-
import random
from time import sleep
import requests
from bs4 import BeautifulSoup
import json
import csv
import datetime
import os
from colorama import Fore, Style, init

init(autoreset=True)

# Const module colorama
RED = Fore.LIGHTRED_EX
GREEN = Fore.LIGHTGREEN_EX
YELLOW = Fore.LIGHTYELLOW_EX
RESET = Style.RESET_ALL

requests.packages.urllib3.disable_warnings()

# Заголовки
headers = {
    "Accept": "*/*",
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    'Request URL': 'https://dm.hybrid.ai/yandexdmp-match',
    'Request Method': 'GET',
    'Status Code': '302',
    'Remote Address': '37.18.16.21:443',
    'Referrer Policy': 'strict-origin-when-cross-origin',
    'access-control-allow-origin': '*',
    'cache-control': 'no-cache, no-store',
    'content-length': '0',
    'date': 'Wed, 19 Oct 2022 21:58:30 GMT',
    'expires': '-1',
    'location': 'https://an.yandex.ru/mapuid/dmphybridai/c74fe4ab13718395574d?sign=304647681',
    'p3p': 'CP="NOI DSP COR CUR ADMa DEVo TAIo PSAo PSDo IVAo IVDo OUR IND COM NAV INT STA OTC"',
    'pragma': 'no-cache',
    'server': 'Hybrid Web Server',
    'x-mode': '106',
    'x-xss-protection': '1; mode=block',
    'authority': 'dm.hybrid.ai',
    'method': 'GET',
    'path': '/yandexdmp-match',
    'scheme': 'https',
    'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'vid=c74fe4ab13718395574d; mkmgsgp=RK0T1G',
    'dnt': '1',
    'referer': 'https://www.avito.ru/',
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'image',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

# Name of folders
F_URLS = 'urls'
F_MOT = 'motorcycles'
F_TRASH = 'trash'


def error_out(s):  # Вывод красного текста
    print(RED + s, sep='')


def done_out(s):  # Вывод зелёного текста
    print(GREEN + s, sep='')


def yellow_out(s):  # Вывод жёлтого текста
    print(YELLOW + s, sep='')


# Создание папок в проекте для данных
def create_dirs():
    if not os.path.exists(F_URLS):  # Creating a folder for copying html page
        os.mkdir(F_URLS)
    if not os.path.exists(F_MOT):  # Creating a folder for film description
        os.mkdir(F_MOT)
    if not os.path.exists(F_TRASH):  # Creating a folder for work(delete)
        os.mkdir(F_TRASH)


# Возвращает Устанавливает заголовки лдя сервера
def get_headers():
    global headers
    resp = requests.get('https://httpbin.org/get')
    for item in resp.headers:
        headers[item] = resp.headers[item]
    resp = requests.get('https://httpbin.org/get', headers={'one': 'true'})
    for item in resp.request.headers:
        headers[item] = resp.request.headers[item]
    # print(headers_1, headers_2, type(headers_1), type(headers_2), sep='\n')
    # global headers
    # headers = dict(headers_1)


# Открывается ли сайт?
def try_open(url):
    print(headers)
    try:
        response = requests.get(url, headers=headers, verify=False)
        sleep(random.uniform(1, 2))
        if response.status_code == 200:
            print('[200] Все хорошо: ' + url)
            print(response.json())
            return True
        else:
            print('[' + str(response.status_code) + '] Не все хорошо: ' + url)
            return False
    except requests.ConnectionError:
        print(f'Сайта {url} не существует')
        return False


# Парсинг каждого отдельного фильма и запись в .csv
def parsing_sites_csv(all_films, year):
    print("Парсинг сайтов фильмов...")
    # Заголовки таблицы
    with open(f"{F_MOT}/Films_{year}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "Название",
                "Страна",
                "Рейтинг",
                "Жанр",
                "Описание",
                "Ссылка"
            )
        )

    # Parsing film sites
    count = 0
    print('\tall_films:', all_films)
    for item in all_films.items():
        print('\tITEM:', item)
        if item[0] == 'Всего фильмов:':
            continue
        title = item[0]
        genre = item[1][0]["Жанр"]
        country = item[1][0]["Страна"]
        rating_num = item[1][0]["Рейтинг"]
        film_href = item[1][0]['Ссылка']
        req = requests.get(url=film_href, headers=headers, verify=False)
        src = req.text

        with open(f"{F_TRASH}/{title}.html", "w", encoding="utf-8") as file:
            file.write(src)

        with open(f"{F_TRASH}/{title}.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        description_p = soup.find("div", class_="visualEditorInsertion filmDesc_editor more_content").find_all("p")
        description = ""
        for words in description_p:
            description += words.text + " "

        # Добавляем данные фильмов
        film_info = list()
        film_info.append(
            {
                "Title": title,
                "Country": country,
                "Rating_num": rating_num,
                "Genre": genre,
                "Description": description,
                "Film_href": film_href
            }
        )

        with open(f"{F_MOT}/Films_{year}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    country,
                    rating_num,
                    genre,
                    description,
                    film_href
                )
            )
        with open(f"{F_MOT}/Films_{year}_1.json", "a", encoding="utf-8") as file:
            json.dump(film_info, file, indent=4, ensure_ascii=False)

        count += 1
        print(f"# Фильм {count} записан...")
        sleep(random.uniform(1, 2))


# Запись словаря фильмов в json файл - Pass
def write_json(films_list, year):
    all_films_dict = {}
    for item in films_list:
        for name in item:
            all_films_dict[name] = item[name]
    with open(f"{F_MOT}/Films_{year}.json", "w", encoding="utf-8") as file:  # windows-1251
        json.dump(all_films_dict, file, indent=4, ensure_ascii=False)


# Основной парсинг сайта
def parse(year):
    all_films_dict = {'Всего фильмов:': 0}

    for page in range(3):
        url = f"https://www.kinoafisha.info/rating/movies/{year}/?page={page}"
        if not try_open(url):
            return
        # print("URL:", url)
        req = requests.get(url, headers=headers, verify=False)
        src = req.text
        # print(src)

        with open(f"{F_URLS}/Films_{year}_{page}.html", "w", encoding="utf-8") as file:
            file.write(src)

        with open(f"{F_URLS}/Films_{year}_{page}.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        all_films = soup.find("div", class_="ratings_list movieList grid_cell9") \
            .find_all("div", class_="movieList_item movieItem movieItem-rating movieItem-position")

        films_count = int(len(all_films))
        if films_count == 0:
            continue

        for item in all_films:
            # print(item)
            about_film = item.find("div", class_="movieItem_info")
            film_name = about_film.find("a", class_="movieItem_title").text
            genre = about_film.find("span", class_="movieItem_genres").text
            country = about_film.find("span", class_="movieItem_year").text
            country = country.split()[1]
            rating_num = about_film.find("span", class_="rating_num").text
            film_href = about_film.find("a", class_="movieItem_title").get("href")
            # film_href = "https://www.kinopoisk.ru" + film_href

            film_info = list()  # List лучше смотрится в json
            film_info.append(
                {
                    "Название": film_name,
                    "Жанр": genre,
                    "Страна": country,
                    "Рейтинг": rating_num,
                    "Ссылка": film_href
                })

            all_films_dict[film_name] = film_info

        # if page == 0:
        #     with open(f"films/Films_{year}.json", "w", encoding="utf-8") as file:  # windows-1251
        #         json.dump(all_films_dict, file, indent=4, ensure_ascii=False)
        # else:
        #     with open(f"films/Films_{year}.json", "a", encoding="utf-8") as file:  # windows-1251
        #         json.dump(all_films_dict, file, indent=4, ensure_ascii=False)

        # with open(f"films/Films_{i}.json", encoding="windows-1251") as file:
        #     all_films = json.load(file)

        # parse_get_trailer(all_films_dict)
        sleep(random.uniform(1, 2))

    all_films_dict['Всего фильмов:'] = len(all_films_dict)
    # parsing_sites_csv(all_films_dict, year)
    with open(f"{F_MOT}/Films_{year}.json", "w", encoding="utf-8") as file:  # windows-1251
        json.dump(all_films_dict, file, indent=4, ensure_ascii=False)
    print(f"Всего фильмов: {len(all_films_dict)}")


# Парсинг сайта авито
def parse_avito():
    all_mot_dict = {'Всего мотоциклов:': 0}
    url = 'https://www.avito.ru/moskva/mototsikly_i_mototehnika/mototsikly/dorozhnye-' \
          'ASgBAgICAkQ80k2~B9RN?cd=1&q=bajaj+pulsar+ns+200&radius=300'
    if not try_open(url):
        return

    req = requests.get(url, headers=headers, verify=False)
    src = req.text
    # src.encoding = 'utf8'
    with open(f"{F_URLS}/Avito_1.html", "w", encoding="utf-8") as file:
        file.write(src)
    with open(f"{F_URLS}/Avito_1.html", encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    all_mots = soup.find("div", class_="items-items-kAJAg") \
        .find_all("div", data_marker="item")

    mots_count = int(len(all_mots))
    all_mot_dict['Всего мотоциклов:'] = len(mots_count)
    print(f"all_mot_dict: {all_mot_dict}\n\nall_mots:\n{all_mots}")
    return


# Начало программы
def main():
    dt_now = datetime.datetime.now()
    now_date = dt_now.day, dt_now.month, dt_now.year
    parse_avito()

    # for year in range(2017, now_year + 1):
    #     print(f"\nПарсинг фильмов за {year} год...")
    #     parse(year)


if __name__ == '__main__':
    hello = YELLOW + " Программа для парсинга объявления мотоциклов(Авито, auto.ru) " + RESET
    print("\n", "{:*^150}".format(hello), "\n", sep='')
    get_headers()
    # create_dirs()
    main()
    # print(f"\n\t{'-' * 20} Done! {'-' * 20}")
    print("\n\t", "{:-^45}".format(' Done! '))
    href_avito = 'https://www.avito.ru/moskva/mototsikly_i_mototehnika/mototsikly/dorozhnye-' \
                 'ASgBAgICAkQ80k2~B9RN?cd=1&q=bajaj+pulsar+ns+200&radius=300'
    href_avito_2 = 'https://www.avito.ru/moskva/mototsikly_i_mototehnika/mototsikly/dorozhnye' \
                   '-ASgBAgICAkQ80k2~B9RN?cd=1&q=bajaj+pulsar+ns+125&radius=300'
