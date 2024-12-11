# -*- coding: utf8 -*-
import random
from time import sleep
import requests
from bs4 import BeautifulSoup
import json
import os
import colorama

# CONST's
colorama.init()
requests.packages.urllib3.disable_warnings()
URL_COCKTAILS = "https://cocktails.bartenders.pro"
NAME_DIR_COCKTAILS_PICS = "Cocktails pics"
WAY_DIR_COCKTAILS_PICS = os.path.join(os.getcwd(), NAME_DIR_COCKTAILS_PICS)

# Заголовки
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}


def create_dir() -> None:
    """ Creating a folder for files """
    if not os.path.exists(WAY_DIR_COCKTAILS_PICS):  # Creating a folder for files
        os.mkdir(WAY_DIR_COCKTAILS_PICS)


# Запись словаря коктейлей в json файл - Pass
def write_json(cocktails_dict: dict) -> None:
    with open(f"Cocktails_IBA.json", "w", encoding="utf-8") as file:  # windows-1251
        json.dump(cocktails_dict, file, indent=4, ensure_ascii=False)


# Открывается ли сайт?
def try_open(url: str) -> [bool, str]:
    try:
        response = requests.get(url)
        sleep(random.uniform(1, 2))
        if response.status_code == 200:
            return True, "[200] Все хорошо"
        else:
            return False, "[" + str(response.status_code) + "] Не все хорошо"
    except requests.ConnectionError:
        return False, f"Сайта {url} не существует"


def try_download_picture(url_pic: str, name_pic: str):
    try:
        img = requests.get(url_pic)
        way_name_pic = os.path.join(WAY_DIR_COCKTAILS_PICS, name_pic + ".jpg")
        img_file = open(way_name_pic, "wb")
        img_file.write(img.content)
        img_file.close()
    except Exception as ex:
        print(f'{ex=}\n{type(ex)=}\n{type(ex).__name__=}')


# Парсинг каждого отдельного коктейля и запись в list
def parsing_cocktail_info(cocktail_url: str, cur_cocktail: int) -> list:
    print('\r', end="")
    print(f"Parsing cocktail №{cur_cocktail}...", end="")
    req = requests.get(url=cocktail_url, headers=headers, verify=False)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    cocktail_local_img_href = soup.find("div", class_="col-lg-12 col-sm-6 col-12").find("img").get("src")
    cocktail_total_img_href = URL_COCKTAILS + cocktail_local_img_href
    cocktail_info = soup.find("div", class_="col-lg-9")
    for_names = cocktail_info.find_all("div")
    cocktail_english_name, cocktail_russian_name = for_names[0].text.strip(), for_names[1].text.strip()
    cocktail_structure = cocktail_info.find("div", class_="table-responsive").find("tbody").find_all("tr")
    cocktail_structure_dict = {}
    for tr in cocktail_structure:
        component, volume = tr.find_all("td")
        cocktail_structure_dict[component.text] = volume.text
    try_download_picture(url_pic=cocktail_total_img_href, name_pic=cocktail_english_name)
    cocktail_info = list()
    cocktail_info.append(
        {
            "English_name": cocktail_english_name,
            "Russian_name": cocktail_russian_name,
            "Img_href": cocktail_total_img_href,
            "Structure": cocktail_structure_dict,
        }
    )
    return cocktail_info


# Основной парсинг сайта
def parse_cocktails() -> None:
    all_cocktails_dict = {"Всего коктейлей:": 0}

    response, mes_response = try_open(URL_COCKTAILS)
    if not response:
        print(mes_response)
        return
    req = requests.get(URL_COCKTAILS, headers=headers, verify=False)
    src = req.text
    # print(src)

    soup = BeautifulSoup(src, "lxml")
    all_cocktails = soup.find("div", class_="col", id="listContainer") \
        .find_all("div", class_="col-lg-2 col-md-3 col-sm-4 col-6 mb-3 pb-3 text-center")

    cocktails_count = int(len(all_cocktails))
    all_cocktails_dict['Всего коктейлей:'] = cocktails_count
    print(f"Всего коктейлей: {cocktails_count}")
    if cocktails_count == 0:
        return
    current_cocktail = 1
    for item in all_cocktails:
        # print(item)
        href_text_cocktail = item.find("a", class_="text-reset text-decoration-none")
        cocktail_name = href_text_cocktail.text.strip()
        cocktail_local_href = href_text_cocktail.get("href")
        cocktail_total_href = URL_COCKTAILS + cocktail_local_href
        cocktail_local_href_img = item.find("img").get("src")
        cocktail_total_href_img = URL_COCKTAILS + cocktail_local_href_img
        cocktail_info = parsing_cocktail_info(cocktail_total_href, current_cocktail)  # List лучше смотрится в json
        all_cocktails_dict[cocktail_name] = cocktail_info
        current_cocktail += 1
        sleep(random.uniform(0.5, 1.1))
    write_json(all_cocktails_dict)


def main() -> None:
    create_dir()
    parse_cocktails()


if __name__ == '__main__':
    main()
    print(f"\n{'-' * 20} Done! {'-' * 20}")
