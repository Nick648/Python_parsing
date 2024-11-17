from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

DRIVER_PATH = 'chromedriver-win64'

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

# service = Service(executable_path='https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/win32/chromedriver-win32.zip')

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://www.ozon.ru/")
print(driver.page_source)
driver.quit()
