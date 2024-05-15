from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

driver = webdriver.Chrome()

url = 'https://ek.ua/ua/list/161/'
driver.get(url)

def extract_product_data(container):
    model = container.find_element(By.CLASS_NAME, 'model-short-title').text
    image_url = container.find_element(By.CLASS_NAME, 'list-img').find_element(By.TAG_NAME, 'img').get_attribute('src')
    shops = container.find_elements(By.CLASS_NAME, 'model-shop-name')
    prices = container.find_elements(By.CLASS_NAME, 'model-shop-price')
    locations = container.find_elements(By.CLASS_NAME, 'model-shop-city')
    data = []
    for shop, price, location in zip(shops, prices, locations):
        shop_name = shop.text.split('\n')[0]
        shop_city = location.text.replace('(', '').replace(')', '')
        price_element = price.find_element(By.TAG_NAME, 'a')
        price_text = price_element.text
        price_value = ''.join(filter(str.isdigit, price_text))

        data.append({
            'Model': model,
            'Image URL': image_url,
            'Shop': shop_name,
            'City': shop_city,
            'Price': price_value
        })
    return data

product_containers = driver.find_elements(By.CLASS_NAME, 'model-short-block')

all_data = []
for container in product_containers:
    product_data = extract_product_data(container)
    all_data.extend(product_data)

csv_file = 'models2.1/bicycle_offers.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Model', 'Image URL', 'Shop', 'City', 'Price'])
    writer.writeheader()
    writer.writerows(all_data)

driver.quit()
