# -*- coding: utf8 -*-
import random
from time import sleep
import requests
from bs4 import BeautifulSoup
import json
import csv
import datetime
import os

requests.packages.urllib3.disable_warnings()

# Заголовки
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}

# Name of folders
F_URLS = 'urls'
F_FILMS = 'films'
F_TRASH = 'trash'


# Создание папок в проекте для данных
def create_dirs():
    if not os.path.exists(F_URLS):  # Creating a folder for copying html page
        os.mkdir(F_URLS)
    if not os.path.exists(F_FILMS):  # Creating a folder for film description
        os.mkdir(F_FILMS)
    if not os.path.exists(F_TRASH):  # Creating a folder for work(delete)
        os.mkdir(F_TRASH)


# Открывается ли сайт?
def try_open(url):
    try:
        response = requests.get(url)
        sleep(random.uniform(1, 2))
        if response.status_code == 200:
            # print('[200] Все хорошо: ' + url)
            return 1
        else:
            # print('[' + str(response.status_code) + '] Не все хорошо: ' + url)
            return 0
    except requests.ConnectionError:
        # print(f'Сайта {url} не существует')
        return 0


# Парсинг каждого отдельного фильма и запись в .csv
def parsing_sites_csv(all_films, year):
    print("Парсинг сайтов фильмов...")
    # Заголовки таблицы
    with open(f"{F_FILMS}/Films_{year}.csv", "w", encoding="utf-8") as file:
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
    for item in all_films.items():
        # print(film_name)
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

        with open(f"{F_FILMS}/Films_{year}.csv", "a", encoding="utf-8") as file:
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
        with open(f"{F_FILMS}/Films_{year}_1.json", "w", encoding="utf-8") as file:
            json.dump(film_info, file, indent=4, ensure_ascii=False)

        count += 1
        print(f"# Фильм {count} записан...")
        sleep(random.uniform(1, 2))


# Найти трейлер на странице фильма - Pass
def parse_get_trailer(all_films_dict):
    for item in all_films_dict:
        film_href = all_films_dict[item][0]['Ссылка']

        req = requests.get(film_href, headers=headers, verify=False)
        src = req.text

        with open(f"href.html", "w", encoding="utf-8") as file:
            file.write(src)

        with open(f"href.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        href = soup.find("a", class_="videoPlayer_playBtn").get('href')
        print(href)
        exit()


# Запись словаря фильмов в json файл - Pass
def write_json(films_list, year):
    all_films_dict = {}
    for item in films_list:
        for name in item:
            all_films_dict[name] = item[name]
    with open(f"{F_FILMS}/Films_{year}.json", "w", encoding="utf-8") as file:  # windows-1251
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

            film_info = list()
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

        # parsing_sites_csv(all_films, year)
        # parse_get_trailer(all_films_dict)
        sleep(random.uniform(1, 2))

    all_films_dict['Всего фильмов:'] = len(all_films_dict)
    with open(f"{F_FILMS}/Films_{year}.json", "w", encoding="utf-8") as file:  # windows-1251
        json.dump(all_films_dict, file, indent=4, ensure_ascii=False)
    print(f"Всего фильмов: {len(all_films_dict)}")


# Начало программы
def main():
    dt_now = datetime.datetime.now()
    now_year = dt_now.year
    # print(dt_now, type(dt_now), dt_now.year, type(dt_now.year))
    for year in range(2017, now_year + 1):
        print(f"\nПарсинг фильмов за {year} год...")
        parse(year)


if __name__ == '__main__':
    create_dirs()
    main()
    print(f"\n{'-' * 20} Done! {'-' * 20}")
