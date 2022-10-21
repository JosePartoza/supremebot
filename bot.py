import requests
import json
import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By



from config import ProductDetails, UserDetails, PaymentDetails

headers = {'user-agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; nl-nl) AppleWebKit/533.17.9 (KHTML, like ''Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5'}

mobile_emulation = {
    "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; nl-nl) AppleWebKit/533.17.9 (KHTML, like Gecko) " 
    "Version/5.0.2 Mobile/8H7 Safari/6533.18.5"
}

prefs = {'disk-cache-size': 4096}

options = Options()
options.add_experimental_option("mobileEmulation", mobile_emulation)
options.add_experimental_option("prefs", prefs)
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ['enable-logging'])
options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

driver = webdriver.Chrome(options=options, service = Service('D:\Python Bot\Supreme Bot\chromedriver.exe'))
wait = WebDriverWait(driver, 10)


def find_item(name):
    url = "https://www.supremenewyork.com/mobile_stock.json"
    html = requests.get(url=url)
    output = json.loads(html.text)
    
    for category in output['products_and_categories']:
        for item in output['products_and_categories'][category]:
            if name in item['name']:
                print(item['name'])
                print(item['id'])
                return item['id']

def get_colour(item_id, colour, size):
    url = f'https://www.supremenewyork.com/shop/{item_id}.json'
    html = requests.get(url=url)
    output = json.loads(html.text)

    for product_colour in output['styles']:
        if colour in product_colour['name']:
            for product_size in product_colour['sizes']:
                if size in product_size['name']:
                    return product_colour['id']

def get_product(item_id, colour_id, size):
    url = 'https://supremenewyork.com/mobile/#products/' + str(item_id) + '/' + str(colour_id)

    driver.get(url)

    wait.until(EC.presence_of_element_located((By.ID, 'size-options')))

    options = Select(driver.find_element_by_id('size-options'))
    options.select_by_visible_text(size)
    driver.find_element(by=By.XPATH, value='//*[@id="cart-update"]/span').click()
    time.sleep(1)
    driver.find_element(by=By.XPATH, value='//*[@id="checkout-now"]').click()

def checkout():
    time.sleep(0.5)
    url = 'https://www.supremenewyork.com/mobile/#checkout'

    driver.get(url)
    wait.until(EC.presence_of_element_located((By.ID, 'order_billing_name')))

    driver.execute_script(
        f'document.getElementById("order_billing_name").value = "{UserDetails.NAME}";'
        f'document.getElementById("order_email").value = "{UserDetails.EMAIL}";'
         f'document.getElementById("order_tel").value = "{UserDetails.TEL}";'
        f'document.getElementById("order_billing_zip").value = "{UserDetails.ZIP}";'
        f'document.getElementById("order_billing_city").value = "{UserDetails.CITY}";'
        f'document.getElementById("order_billing_address").value = "{UserDetails.ADDRESS}";'
        f'document.getElementById("credit_card_number").value = "{PaymentDetails.CARD_NUMBER}";'
        f'document.getElementById("credit_card_cvv").value = "{PaymentDetails.CVV}";'
    )

    # card_type = Select(driver.find_element_by_id('credit_card_type'))
    # card_type.select_by_visible_text(str(PaymentDetails.CARD_TYPE))

    card_month = Select(driver.find_element_by_id('credit_card_month'))
    card_month.select_by_value(str(PaymentDetails.MONTH))

    card_year = Select(driver.find_element_by_id('credit_card_year'))
    card_year.select_by_value(str(PaymentDetails.YEAR))

    driver.find_element_by_xpath('//*[@id="order_terms"]').click()

    driver.find_element_by_xpath('//*[@id="submit_button"]').click()
    

if __name__ == '__main__':
    t0 = time.time()
    item_id = find_item(ProductDetails.KEYWORDS)
    colour_id = get_colour(item_id, ProductDetails.COLOUR, ProductDetails.SIZE)
    get_product(item_id, colour_id, ProductDetails.SIZE)
    checkout()
    print('TIME: ', time.time()-t0)