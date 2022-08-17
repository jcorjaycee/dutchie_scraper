from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

DRIVER_PATH = 'chromedriver.exe'

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://dutchie.com/stores/tweed-london/products/vaporizers")

DUTCHIE_KEY_PRODUCT_BRAND = "bUxuOp"
DUTCHIE_KEY_PRODUCT_NAME = "kjymBK"
DUTCHIE_KEY_PRODUCT_PRICE = "hJFddt"
DUTCHIE_KEY_PRODUCT_BUTTON_SINGLE = "zdtBd"
DUTCHIE_KEY_PRODUCT_BUTTON_DOUBLE = "esCRpt"
DUTCHIE_KEY_PRODUCT_STRAINTYPE = "gfWvo"
DUTCHIE_KEY_PRODUCT_CONCENTRATIONS = "hdncuE"
DUTCHIE_KEY_PAGE_BUTTON = "cwWhSO"
DUTCHIE_KEY_PAGE_NEXT = "hjQwsb"
DUTCHIE_KEY_PAGE_PREV = "deZqfc"

def dutchie_get_num_pages():
	page_buttons = driver.find_elements(By.CLASS_NAME, DUTCHIE_KEY_PAGE_BUTTON)
	return int(page_buttons[-1].text)

for page in range(dutchie_get_num_pages()):
	print("\n\nPage " + str(page + 1) + "\n\n")
	scrollLevel = 0

	height = int(driver.execute_script("return document.documentElement.scrollHeight"))

	while scrollLevel < height:
		scrollLevel += 1000
		driver.execute_script("window.scrollTo(0," + str(scrollLevel) + ")")
		time.sleep(0.2)

	# TODO: Some items have multiple sizes available. These will currently
	# mess with the dataset, as the current design only accounts for one price
	# per product
	item_names = driver.find_elements(By.CLASS_NAME, DUTCHIE_KEY_PRODUCT_NAME)
	item_prices = driver.find_elements(By.CLASS_NAME, DUTCHIE_KEY_PRODUCT_PRICE)

	if (len(item_names) < len(item_prices)):
		print("\n\nWARNING: More prices found than items. It appears there " +
			"are some items with multiple sizes. The price display will be incorrect.\n\n")

	for item in range(len(item_names)):
		print(item_names[item].text + " - " + item_prices[item].text)
	print("\n")

	if page < dutchie_get_num_pages():
		driver.find_element(By.CLASS_NAME, DUTCHIE_KEY_PAGE_NEXT).click()
		time.sleep(3)

driver.quit()