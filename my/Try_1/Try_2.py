# -*- coding: utf8 -*-
import random
from time import sleep
import requests
from bs4 import BeautifulSoup
import json
# import csv
import datetime
import os

requests.packages.urllib3.disable_warnings()
dt_now = datetime.datetime.now()
now_year = dt_now.year
# print(dt_now, type(dt_now), dt_now.year, type(dt_now.year))

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}


def create_dirs():
    if not os.path.exists("urls"):  # Creating a folder for copying html page
        os.mkdir("urls")
    if not os.path.exists("films"):  # Creating a folder for film description
        os.mkdir("films")
    if not os.path.exists("trash"):  # Creating a folder for work(delete)
        os.mkdir("trash")


def try_open(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print('[200] Все хорошо: ' + url)
        else:
            print('[' + str(response.status_code) + '] Не все хорошо: ' + url)
    except requests.ConnectionError:
        print(f'Сайта {url} не существует')


def main():
    for i in range(2020, now_year + 1):
        print(f"Парсим фильмы за {i} год...")
        url = f"https://www.kinoafisha.info/rating/movies/{i}/"
        # print("URL:", url)
        req = requests.get(url, headers=headers, verify=False)
        src = req.text
        # print(src)

        with open(f"urls/Films_{i}.html", "w", encoding="utf-8") as file:
            file.write(src)

        with open(f"urls/Films_{i}.html", encoding="utf-8") as file:
            src = file.read()

        sleep(random.randrange(1, 3))

        soup = BeautifulSoup(src, "lxml")
        all_films = soup.find("div", class_="ratings_list movieList grid_cell9") \
            .find_all("div", class_="movieList_item movieItem movieItem-rating movieItem-position")

        all_films_dict = {}
        for item in all_films:
            film_info = list()
            # print(item)
            about_film = item.find("div", class_="movieItem_info")
            film_name = about_film.find("a", class_="movieItem_title").text
            genre = about_film.find("span", class_="movieItem_genres").text
            country = about_film.find("span", class_="movieItem_year").text
            rating_num = about_film.find("span", class_="rating_num").text
            film_href = about_film.find("a", class_="movieItem_title").get("href")
            # film_href = "https://www.kinopoisk.ru" + film_href
            # item_href = "https://health-diet.ru" + item.get("href")
            film_info.append(
                {
                    "Название": film_name,
                    "Жанр": genre,
                    "Страна": country,
                    "Рейтинг": rating_num,
                    "Ссылка": film_href
                })

            all_films_dict[film_name] = film_info  # item_href

        with open(f"films/Films_{i}.json", "w", encoding="windows-1251") as file:
            json.dump(all_films_dict, file, indent=4, ensure_ascii=False)

        with open(f"films/Films_{i}.json", encoding="windows-1251") as file:
            all_films = json.load(file)

        iteration_count = int(len(all_films))
        count = 0
        print(f"Всего фильмов: {iteration_count}")

        # for film_name, film_href in all_films.items():
        #     req = requests.get(url=film_href, headers=headers, verify=False)
        #     src = req.text
        #
        #     with open(f"trash/{film_name}.html", "w", encoding="utf-8") as file:
        #         file.write(src)
        #
        #     with open(f"trash/{film_name}.html", encoding="utf-8") as file:
        #         src = file.read()
        #
        #     soup = BeautifulSoup(src, "lxml")
        #
        #     # проверка страницы на наличие таблицы с продуктами
        #     title = soup.find("h1",
        #                       class_="styles_title__65Zwx styles_root__l9kHe styles_root__5sqsd styles_rootInDark__SZlor")
        #     title = title.find("span").text
        #     print(title)
        #     description = soup.find("p", class_="styles_root__aZJRN").text
        #     print(description)
        #     rows = soup.find("div", data_test_id="encyclopedic-table").find_all("div",
        #                                                                         class_="styles_rowLight__P8Y_1 styles_row__da_RK")
        #     print(rows)
        #     country = rows.find_all("div", class_="styles_valueLight__nAaO3 styles_value__g6yP4")
        #     country = country.find("a", class_="styles_linkLight__cha3C styles_link__3QfAk").text
        #     genre = rows.find_all("div", class_="styles_valueLight__nAaO3 styles_value__g6yP4")
        #     iteration_count -= 1
        #     print(f"Осталось итераций: {iteration_count}")
        #     sleep(random.randrange(1, 3))


"""
            # собираем заголовки таблицы
            table_head = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")
            product = table_head[0].text
            calories = table_head[1].text
            proteins = table_head[2].text
            fats = table_head[3].text
            carbohydrates = table_head[4].text

            with open(f"data/{count}_{category_name}.csv", "w", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        product,
                        calories,
                        proteins,
                        fats,
                        carbohydrates
                    )
                )

            # собираем данные продуктов
            products_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")

            product_info = []
            for item in products_data:
                product_tds = item.find_all("td")

                title = product_tds[0].find("a").text
                calories = product_tds[1].text
                proteins = product_tds[2].text
                fats = product_tds[3].text
                carbohydrates = product_tds[4].text

                product_info.append(
                    {
                        "Title": title,
                        "Calories": calories,
                        "Proteins": proteins,
                        "Fats": fats,
                        "Carbohydrates": carbohydrates
                    }
                )

                with open(f"data/{count}_{category_name}.csv", "a", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        (
                            title,
                            calories,
                            proteins,
                            fats,
                            carbohydrates
                        )
                    )
            with open(f"data/{count}_{category_name}.json", "a", encoding="utf-8") as file:
                json.dump(product_info, file, indent=4, ensure_ascii=False)

            count += 1
            print(f"# Итерация {count}. {category_name} записан...")
            iteration_count = iteration_count - 1

            if iteration_count == 0:
                print("Работа завершена")
                break
"""

if __name__ == '__main__':
    create_dirs()
    main()
