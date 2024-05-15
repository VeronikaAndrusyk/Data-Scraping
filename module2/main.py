from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time

# Ініціалізація драйвера Chrome
driver = webdriver.Chrome()

# URL сторінки з пропозиціями телевізорів
url = 'https://ek.ua/ua/list/160/'
driver.get(url)

# Очікуємо завантаження сторінки
time.sleep(5)

# Функція для отримання даних про кожну пропозицію телевізора
def extract_tv_data(container):
    model = container.find_element(By.CLASS_NAME, 'model-short-title').text
    image_url = container.find_element(By.CLASS_NAME, 'list-img').find_element(By.TAG_NAME, 'img').get_attribute('src')
    shops = container.find_elements(By.CLASS_NAME, 'model-shop-name')
    prices = container.find_elements(By.CLASS_NAME, 'model-shop-price')
    locations = container.find_elements(By.CLASS_NAME, 'model-shop-city')
    data = []
    for shop, price, location in zip(shops, prices, locations):
        shop_name = shop.text.split('\n')[0]
        shop_city = location.text.replace('(', '').replace(')', '')
        price_text = price.text
        price_value = ''.join(filter(str.isdigit, price_text))
        data.append({
            'Model': model,
            'Image URL': image_url,
            'Shop': shop_name,
            'City': shop_city,
            'Price': price_value
        })
    return data

# Збір даних з кожної пропозиції телевізора
tv_containers = driver.find_elements(By.CLASS_NAME, 'model-short-block')
all_tv_data = []
for container in tv_containers:
    tv_data = extract_tv_data(container)
    all_tv_data.extend(tv_data)

# Закриття драйвера після збору даних
driver.quit()

# Збереження зібраних даних у CSV-файл
csv_file = 'tv_offers.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Model', 'Image URL', 'Shop', 'City', 'Price'])
    writer.writeheader()
    writer.writerows(all_tv_data)

print("Data saved to", csv_file)
