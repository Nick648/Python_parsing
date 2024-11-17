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

# Headers
headers = '''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7
Cache-Control: max-age=0
Connection: keep-alive
Cookie: gdpr=0; _ym_uid=1666473224225800089; spravka=dD0xNjY2NDczMjM4O2k9ODkuMTg4LjE3OS4xODc7RD0zOEMzNEZFQjVFMzYwQzc0REEyQjU1RUFEOTFBRTk4M0YwMDgwMEU4RDY5REIzOEMxMjc2NDE1MUJFN0FFOEYyNzVFREQwN0E7dT0xNjY2NDczMjM4MDQ5NzYyNDU0O2g9MzA0ZDFiYTRiODM4MDE3ZDNiMjc2ZWNlY2M0MmY3ZTA=; suid=5c8b8b8d566b4144df54716a14ebd78e.7b747f7c0c294c4ff74f73560399a87f; autoruuid=g63545d162d6lun69gmef9fbqajb1vlr.bf544821dc7e407cea3c6e26b07aa21b; yuidlt=1; yandexuid=9509775751666431348; crookie=U0NuWoZIefwQeJqgUbcD4SIHHt0Vhb51OhVpNdczfcJrgp31mzw/g4QCImqPU7Es8OpsXoPNPQHbWFfuuj3nQDOguzk=; cmtchd=MTY2NjQ3MzIzOTk4OQ==; yandex_login=dimitriy648; i=WFDPDiTB7ZtCd/LpRxL6/bO2td8Mx1PQN/mFJspA2otmfGpR4J1vW0+K8JsCgz/tfbqSLISOq2hwuOxy/GtbSqmnjtg=; autoru_sid=73658921%7C1666473283862.7776000.TXfgXWfhZd6sZuBQlOOMeQ.YUG8_tOnKdaH94QRRSaU7So2o_0fdtHjlX_jIGQX3Uk; autoru-visits-count=1; _ym_isad=2; _csrf_token=95439d67157b38cfa0eda990a1cb11f9a9a18ba43fd9e9f5; Session_id=3:1666724120.5.0.1666431991381:u7O8WQ:2b.1.2:1|918655262.0.2|61:10008375.20183.bCbqg6qwgcZYpafg4w6t_3dcTns; mda2_beacon=1666724120463; sso_status=sso.passport.yandex.ru:synchronized; pdd_exam_popup_hide=true; from=morda; ys=udn.cDpkaW1pdHJpeTY0OA%3D%3D%23wprid.1666729074374505-17765231773322694036-sas2-0105-sas-l7-balancer-8080-BAL-3988%23c_chck.158185053; _yasc=wfg9OtSxO4Q8GzMXV9ZyG2C+owq86rT+QkHcK1e8rNrFIPDK/Hi5tIvZ5S2H5w==; gids=10765; gradius=300; from_lifetime=1666729117497; _ym_d=1666729117; layout-config={"win_width":1348,"win_height":937}; cycada=42VhJ+YGSZyID0XLP9/P/qfOjcxzlLtGCfvXUjCivjo=
DNT: 1
Host: auto.ru
Referer: https://auto.ru/schelkovo/motorcycle/bajaj/pulsar/all/?query=bajaj%20pulsar%20ns200&from=searchline
sec-ch-ua: "Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36
'''.strip().split("\n")

# headers = '''
# Accept: */*
# Accept-Encoding: gzip, deflate, br
# Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7
# Connection: keep-alive
# Content-Length: 93
# content-type: application/json
# Cookie: gdpr=0; _ym_uid=1666473224225800089; spravka=dD0xNjY2NDczMjM4O2k9ODkuMTg4LjE3OS4xODc7RD0zOEMzNEZFQjVFMzYwQzc0REEyQjU1RUFEOTFBRTk4M0YwMDgwMEU4RDY5REIzOEMxMjc2NDE1MUJFN0FFOEYyNzVFREQwN0E7dT0xNjY2NDczMjM4MDQ5NzYyNDU0O2g9MzA0ZDFiYTRiODM4MDE3ZDNiMjc2ZWNlY2M0MmY3ZTA=; suid=5c8b8b8d566b4144df54716a14ebd78e.7b747f7c0c294c4ff74f73560399a87f; autoruuid=g63545d162d6lun69gmef9fbqajb1vlr.bf544821dc7e407cea3c6e26b07aa21b; yuidlt=1; yandexuid=9509775751666431348; crookie=U0NuWoZIefwQeJqgUbcD4SIHHt0Vhb51OhVpNdczfcJrgp31mzw/g4QCImqPU7Es8OpsXoPNPQHbWFfuuj3nQDOguzk=; cmtchd=MTY2NjQ3MzIzOTk4OQ==; yandex_login=dimitriy648; i=WFDPDiTB7ZtCd/LpRxL6/bO2td8Mx1PQN/mFJspA2otmfGpR4J1vW0+K8JsCgz/tfbqSLISOq2hwuOxy/GtbSqmnjtg=; autoru_sid=73658921%7C1666473283862.7776000.TXfgXWfhZd6sZuBQlOOMeQ.YUG8_tOnKdaH94QRRSaU7So2o_0fdtHjlX_jIGQX3Uk; autoru-visits-count=1; _ym_isad=2; _csrf_token=95439d67157b38cfa0eda990a1cb11f9a9a18ba43fd9e9f5; from=direct; Session_id=3:1666724120.5.0.1666431991381:u7O8WQ:2b.1.2:1|918655262.0.2|61:10008375.20183.bCbqg6qwgcZYpafg4w6t_3dcTns; ys=udn.cDpkaW1pdHJpeTY0OA%3D%3D#c_chck.158185053; mda2_beacon=1666724120463; sso_status=sso.passport.yandex.ru:synchronized; layout-config={"win_width":1365,"win_height":937}; pdd_exam_popup_hide=true; _yasc=Twln0Vgc5SNobwfgZ2EfZZZwoPuyzAo7k2gkR3Hdenyo68hij/JasJOE+eW7Tw==; cycada=1RNC+AIsTyLsuIiQidO35afOjcxzlLtGCfvXUjCivjo=; from_lifetime=1666724646872; _ym_d=1666724646
# DNT: 1
# Host: auto.ru
# Origin: https://auto.ru
# Referer: https://auto.ru/schelkovo/motorcycle/bajaj/pulsar/all/?query=bajaj%20pulsar%20&from=searchline
# sec-ch-ua: "Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"
# sec-ch-ua-mobile: ?0
# sec-ch-ua-platform: "Windows"
# Sec-Fetch-Dest: empty
# Sec-Fetch-Mode: same-origin
# Sec-Fetch-Site: same-origin
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36
# x-client-app-version: 185.0.10210752
# x-client-date: 1666724649642
# x-csrf-token: 95439d67157b38cfa0eda990a1cb11f9a9a18ba43fd9e9f5
# x-page-request-id: 428cf7ec448bd6610389fca9816452e1
# x-requested-with: XMLHttpRequest
# x-retpath-y: https://auto.ru/schelkovo/motorcycle/bajaj/pulsar/all/?query=bajaj%20pulsar%20&from=searchline
# '''.strip().split("\n")

dict_headers = {}
for header in headers:
    key, value = header.split(': ')
    dict_headers[key] = value

# Name of folders
F_URLS = os.path.join(os.path.abspath(__file__), '..', 'urls')
F_MOT = os.path.join(os.path.abspath(__file__), '..', 'motorcycles')
F_TRASH = os.path.join(os.path.abspath(__file__), '..', 'trash')


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


# Открывается ли сайт?
def try_open(url):
    try:
        response = requests.get(url, headers=dict_headers, verify=False)
        sleep(random.uniform(1, 2))
        if response.status_code == 200:
            # print(f'Response [200] Все хорошо: {url}')
            return True
        else:
            print(f'Response [{response.status_code}] Не все хорошо: {url}')
            return False
    except requests.ConnectionError:
        print(f'Сайта {url} не существует')
        return False


# Запись словаря фильмов в json файл - Pass
def write_json(films_list, year):
    all_films_dict = {}
    for item in films_list:
        for name in item:
            all_films_dict[name] = item[name]
    with open(f"{F_MOT}/Films_{year}.json", "w", encoding="utf-8") as file:  # windows-1251
        json.dump(all_films_dict, file, indent=4, ensure_ascii=False)


# Основной парсинг сайта
def parse_bike(url):
    req = requests.get(url, headers=dict_headers, verify=False)
    req.encoding = 'utf-8'  # 'cp1251'
    src = req.text
    print(url)
    # src = req.content
    soup = BeautifulSoup(src, "lxml")
    main_page = soup.find("div", class_="PageCard")
    title_name = main_page.find("h1", class_="CardHead__title").text
    try:
        date_title = main_page.find("div", class_="CardHead__infoItem CardHead__creationDate").get("title")
        date_text = main_page.find("div", class_="CardHead__infoItem CardHead__creationDate").text
    except AttributeError:  # 'NoneType' object has no attribute 'get'
        date_title, date_text = None, None

    ad_id_title = main_page.find("div", class_="CardHead__infoItem CardHead__id").get("title")
    ad_id_text = main_page.find("div", class_="CardHead__infoItem CardHead__id").text
    try:
        seller_name_title = main_page.find("div", class_="CardSellerNamePlace__name").get("title")
        seller_name_text = main_page.find("div", class_="CardSellerNamePlace__name").text
        avatar = main_page.find("img", class_="CardSellerNamePlace__avatar-icon").get("src")
    except AttributeError:  # 'NoneType' object has no attribute 'get'
        seller_name_title, seller_name_text, avatar = None, None, None

    price = main_page.find("span", class_="OfferPriceCaption__price")
    price_text = main_page.find("span", class_="OfferPriceCaption__price").text
    place = main_page.find("div",
                           class_="CardSellerNamePlace__address")
    place_text = main_page.find("div",
                                class_="CardSellerNamePlace__address").text
    about_bike = main_page.find("div", class_="CardOfferBody__columnsWrapper")
    card_info = about_bike.find("ul", class_="CardInfo")
    release_year = card_info.find("li", class_="CardInfoRow CardInfoRow_year").find("a",
                                                                                    class_="Link Link_color_black").text
    try:
        km_age = card_info.find("li", class_="CardInfoRow CardInfoRow_kmAge").find("span", class_="CardInfoRow__cell")
        km_age_text = card_info.find("li", class_="CardInfoRow CardInfoRow_kmAge").find("span",
                                                                                        class_="CardInfoRow__cell").text
    except AttributeError:  # 'NoneType' object has no attribute 'get'
        km_age, km_age_text = None, None

    color = card_info.find("li", class_="CardInfoRow CardInfoRow_color").find("a",
                                                                              class_="Link Link_color_black").text
    engine = card_info.find("li", class_="CardInfoRow CardInfoRow_engine").find("a", class_="CardInfoRow__cell")
    engine_text = card_info.find("li", class_="CardInfoRow CardInfoRow_engine").find("a",
                                                                                     class_="CardInfoRow__cell").text
    condition = card_info.find("li", class_="CardInfoRow CardInfoRow_state").find("a", class_="CardInfoRow__cell").text
    owners = card_info.find("li", class_="CardInfoRow CardInfoRow_ownersCount").find("a",
                                                                                     class_="CardInfoRow__cell").text
    pts = card_info.find("li", class_="CardInfoRow CardInfoRow_pts").find("a", class_="CardInfoRow__cell").text

    params = card_info.find_all("li")
    # params = [item.text for item in params]

    image_gallery = about_bike.find("div", class_="ImageGalleryDesktop")
    images = image_gallery.find_all("img", class_="ImageGalleryDesktop__image ImageGalleryDesktop__image_hidden")

    description = main_page.find("div", class_="CardDescription CardOfferBody__contentIsland") \
        .find("div", class_="CardDescriptionHTML").find("span").text

    reviews = main_page.find("div", id="reviews").find("div", class_="RatingInfo RatingInfo_size_normal") \
        .find("div", class_="ReviewRating__number").text

    print(f'{"*" * 30}\n'
          f'Name: {title_name}\n'
          f'{date_title}: {date_text}\n'
          f'{ad_id_title}: {ad_id_text}\n'
          f'{seller_name_title}: {seller_name_text}\n'
          f'Price(): {price}\n'
          f'Price: {price_text}\n'
          f'avatar: {avatar}\n'
          f'place(): {place}\n'
          f'place_text: {place_text}\n'
          f'release_year: {release_year}\n'
          f'Пробег(): {km_age}\n'
          f'Пробег: {km_age_text}\n'
          f'Цвет: {color}\n'
          f'Двигатель(): {engine}\n'
          f'engine_text: {engine_text}\n'
          f'Состояние: {condition}\n'
          f'Владельцы: {owners}\n'
          f'ПТС: {pts}\n'
          f'ПТС: {pts}\n'
          f'Комментарий продавца: {description}\n'
          f'Рейтинг: {reviews}\n'
          f'Link: {url}\n'
          f'{"*" * 30}')

    bike_info = list()  # List лучше смотрится в json
    bike_info.append(
        {
            "Название": title_name,
            "Цена": price,
            "Год": release_year,
            "Пробег": km_age,
            # "Параметры": params,
            "Ссылка": url
        })

    return bike_info


def check_en(data):  # Pass
    final = ''
    for i in data:
        if i.isascii():
            final += i
        elif ord(i) == 160:
            final += ' '
        # print(f'{i}: {i.isalnum()}, {ord(i)}')
    return final


# Pass
def other():
    pass
    # desc = bike.find("div", class_="ListingItem__description")
    # # link = desc.find("a", class_="Link ListingItemTitle__link").get("href")
    # name = desc.find("a", class_="Link ListingItemTitle__link").text
    # params = desc.find("div", class_="ListingItemTechSummaryDesktop ListingItem__techSummary") \
    #     .find_all("div", class_="ListingItemTechSummaryDesktop__cell")
    # params = [item.text for item in params]
    # price = desc.find("div", class_="ListingItem__priceBlock").find("a", class_="Link ListingItemPrice__link").text
    # year = desc.find("div", class_="ListingItem__year").text
    # km_age = desc.find("div", class_="ListingItem__kmAge").text

    # price = check_en(price)
    # km_age = check_en(km_age)
    # for j in range(len(params)):
    #     params[j] = check_en(params[j])

    # print(f'{"*" * 30}\n'
    #       f'Name: {name}\n'
    #       f'Price: {price}\n'
    #       f'Year: {year}\n'
    #       f'Km_age: {km_age}\n'
    #       f'Parameters: {params}\n'
    #       f'Link: {link}\n'
    #       f'{"*" * 30}')

    # print(price)
    # for i in price:
    #     print(f'{i}: {ord(i)}')

    # bike_info = list()  # List лучше смотрится в json
    # bike_info.append(
    #     {
    #         "Название": name,
    #         "Цена": price,
    #         "Год": year,
    #         "Пробег": km_age,
    #         "Параметры": params,
    #         "Ссылка": link
    #     })


# Парсинг сайта auto.ru
def parse_auto_ru():
    all_mot_dict = {'Всего мотоциклов:': 0}
    url = 'https://auto.ru/schelkovo/motorcycle/bajaj/pulsar/all/?sort=price-asc'

    # if not try_open(url):
    #     return

    req = requests.get(url, headers=dict_headers, verify=False)
    req.encoding = 'utf-8'  # 'cp1251'
    src = req.text

    # with open(f"{F_URLS}/Auto_ru_1.html", "w", encoding='latin-1') as file:  # 'latin-1'  ISO-8859-1
    #     file.write(src)
    # with open(f"{F_URLS}/Auto_ru_1.html", encoding='utf-8') as file:
    #     src = file.read()
    # src = req.content

    soup = BeautifulSoup(src, "lxml")
    all_mots = soup.find("div", class_="ListingCars ListingCars_outputType_list").find_all("div", class_="ListingItem")
    count = 0
    for bike in all_mots:
        count += 1
        link = bike.find("div", class_="ListingItem__main").find("a", class_="Link OfferThumb").get("href")

        print(link)
        exit()
        bike_info = parse_bike(link)

        other()  # !!!!!!!!!!!!!!!!
        break

        all_mot_dict[count] = bike_info

    all_mot_dict['Всего мотоциклов:'] = len(all_mot_dict) - 1
    with open(f"{F_MOT}/Parse.json", "w", encoding='utf-8') as file:  # windows-1251
        json.dump(all_mot_dict, file, indent=4, ensure_ascii=False)
    # print(f"Всего мотоциклов: {len(all_mot_dict)-1}")


def try_post():  # Fail for auto.ru
    url = 'https://auto.ru/-/ajax/desktop/searchlineSuggest/'

    params = {'category': "moto",
              'query': "bajaj pulsar ",
              'section': "all",
              'geo_radius': 200,
              'geo_id': [10765]}
    res = requests.post(url, json=params, headers=dict_headers)
    print(res.status_code, res.request)
    print(res.json())
    exit()


def try_session():
    from requests_html import HTMLSession

    url = 'https://auto.ru/schelkovo/motorcycle/bajaj/pulsar/all/?sort=price-asc'
    session = HTMLSession()
    r = session.get(url, headers=dict_headers)
    r.encoding = 'latin1'
    print(f'URL: {url}')

    r.html.render()  # run javascript
    ans = r
    ht_ml = r.text  # <class 'str'>
    ht_ml_1 = r.html  # <class 'requests_html.HTML'>

    # print(ans, '\n', ht_ml)

    # l = r.html.absolute_links
    # l_1 = r.html.links
    # print(len(l), type(l))
    # print(len(l_1), type(l_1))
    # for e in l:
    #     print(e)
    # print('8' * 40)
    # for e in l_1:
    #     print(e)

    with open(f"{F_URLS}/Auto_ru_11.html", "w", encoding='latin1') as file:  # 'latin-1'  ISO-8859-1
        file.write(r.text)
    # with open(f"{F_URLS}/Auto_ru_11.html", encoding='utf-8') as file:
    #     src = file.read()

    # src = r.content
    # print(type(src), len(src), src)

    page_list = r.html.find('.listing-filters')
    print(page_list, type(page_list))

    # about = r.html.find('#donate-button', first=True) #   . = class  # = id
    # about_1 = r.html.find('#donate-button', first=True).text
    # about_2 = r.html.find('#donate-button', first=True).attrs
    # about_3 = r.html.find('#donate-button', first=True).html
    # about_4 = r.html.find('#donate-button', first=True).tag

    # text = r.html.search('Calculations are {} with')[0] # find word
    # text_1 = r.html.xpath("")


# Начало программы
def main():
    # dt_now = datetime.datetime.now()
    # now_date = dt_now.day, dt_now.month, dt_now.year

    # parse_auto_ru()
    try_session()


if __name__ == '__main__':
    hello = YELLOW + " Программа для парсинга объявления мотоциклов(Авито, auto.ru) " + RESET
    print("\n", "{:*^150}".format(hello), "\n", sep='')
    # get_headers()
    # create_dirs()
    main()
    # print("\n\t", "{:-^45}".format(' Done! '))
