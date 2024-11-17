from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver
from undetected_chromedriver import By
import time
import pyautogui as pg
import keyboard

url_test = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'


def try_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')
    options.add_argument('--disable-blink-features=AutomationControlled')

    # driver = webdriver.Chrome(
    #     executable_path='',
    #     options=options
    # )

    s = Service(executable_path='')
    driver = webdriver.Chrome(service=s, options=options)

    try:
        driver.get(url_test)
        time.sleep(10)
    except Exception as ex:
        print(f'{type(ex).__name__} -> {type(ex)} -> {ex}')
    finally:
        driver.close()
        driver.quit()


def try_undetected_driver():
    try:
        driver = undetected_chromedriver.Chrome()
        driver.get(url_test)
        time.sleep(10)
    except Exception as ex:
        print(f'{type(ex).__name__} -> {type(ex)} -> {ex}')
    finally:
        driver.close()
        driver.quit()


def check_robot_control() -> None:
    time.sleep(3)
    find_control_window = pg.locateOnScreen('data/control.png', confidence=0.85)
    if find_control_window:
        pg.moveTo(find_control_window, duration=0.1)
        find_control_button = pg.locateOnScreen('data/button.png', confidence=0.85, region=find_control_window)
        if find_control_button:
            pg.moveTo(find_control_button, duration=0.1)
            pg.click(clicks=1, interval=0.1)


def auto_ru_parse():
    url = 'https://auto.ru/schelkovo/motorcycle/bajaj/pulsar/all/?sort=price-asc'
    try:
        driver = undetected_chromedriver.Chrome()
        driver.get(url)
        check_robot_control()
        keyboard.wait('Esc')
        mot_list = driver.find_element(By.CLASS_NAME, 'ListingCars__loaderOverlay')
        for el in mot_list:
            print(el)
        time.sleep(10)
    except Exception as ex:
        print(f'{type(ex).__name__} -> {type(ex)} -> {ex}')
    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    # try_selenium()
    # try_undetected_driver()
    auto_ru_parse()
