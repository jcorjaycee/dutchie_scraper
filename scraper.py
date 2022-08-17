from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

DRIVER_PATH = 'chromedriver.exe'

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://dutchie.com/stores/STORENAMEHERE")

DUTCHIE_KEY_PRODUCT_CELL = "jTzrhU"
DUTCHIE_KEY_PRODUCT_BRAND = "bUxuOp"
DUTCHIE_KEY_PRODUCT_NAME = "kjymBK"
DUTCHIE_KEY_PRODUCT_SIZE = "hYKiO"
DUTCHIE_KEY_PRODUCT_PRICE = "hJFddt"
DUTCHIE_KEY_PRODUCT_BUTTON_SINGLE = "zdtBd"
DUTCHIE_KEY_PRODUCT_BUTTON_DOUBLE = "esCRpt"
DUTCHIE_KEY_PRODUCT_STRAINTYPE = "gfWvo"
DUTCHIE_KEY_PRODUCT_CONCENTRATIONS = "hdncuE"
DUTCHIE_KEY_PAGE_BUTTON = "cwWhSO"
DUTCHIE_KEY_PAGE_NEXT = "hjQwsb"
DUTCHIE_KEY_PAGE_PREV = "deZqfc"

productList = []


class Product:
    def __init__(self, brand, name, sizes, prices):
        self.brand = brand
        self.name = name
        self.sizes = sizes
        self.prices = prices

    def toString(self):
        string_build = self.brand.ljust(30, ' ') + self.name.ljust(30, ' ')
        if len(self.sizes) > 0:
            for i in range(len(self.sizes)):
                string_build += "\n" + self.sizes[i].rjust(45, ' ') + self.prices[i].rjust(5, ' ')
        else:
            string_build += self.prices[0]
        return string_build


def dutchie_get_num_pages():
    page_buttons = driver.find_elements(By.CLASS_NAME, DUTCHIE_KEY_PAGE_BUTTON)
    if len(page_buttons) == 0:
        return 0
    return int(page_buttons[-1].text) - 1


for page in range(dutchie_get_num_pages() + 1):
    print("Processing page " + str(page + 1))
    scrollLevel = 0

    height = int(driver.execute_script("return document.documentElement.scrollHeight"))

    while scrollLevel < height:
        scrollLevel += 1000
        driver.execute_script("window.scrollTo(0," + str(scrollLevel) + ")")
        time.sleep(0.2)

    cells = driver.find_elements(By.CLASS_NAME, DUTCHIE_KEY_PRODUCT_CELL)

    for cell in cells:
        product_brand = cell.find_element(By.CLASS_NAME, DUTCHIE_KEY_PRODUCT_BRAND).text
        product_name = cell.find_element(By.CLASS_NAME, DUTCHIE_KEY_PRODUCT_NAME).text
        # have to grab size/price lists separately as otherwise the lists will go stale when referencing later on
        # cannot grab .text directly due to the plural find_elements method
        product_sizes_list = cell.find_elements(By.CLASS_NAME, DUTCHIE_KEY_PRODUCT_SIZE)
        product_prices_list = cell.find_elements(By.CLASS_NAME, DUTCHIE_KEY_PRODUCT_PRICE)

        product_sizes = []
        product_prices = []

        for index, price in enumerate(product_prices_list):
            if len(product_sizes_list) > 0:
                product_sizes.append(product_sizes_list[index].text)
            product_prices.append(price.text)

        newProduct = Product(product_brand, product_name, product_sizes, product_prices)
        productList.append(newProduct)

    if page < dutchie_get_num_pages():
        driver.find_element(By.CLASS_NAME, DUTCHIE_KEY_PAGE_NEXT).click()
        time.sleep(0.2)

print(str(len(productList)) + " items added. Here is the list.")

print("Brand".ljust(30, ' ') + "Name".ljust(30, ' '))

for index, product in enumerate(productList):
    print(productList[index].toString())

driver.quit()
