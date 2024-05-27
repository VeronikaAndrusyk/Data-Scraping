import csv
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

csv_filename = 'exchange_rates_last_3_months.csv'

with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['ДАТА', 'КОД', 'ПОЗНАЧЕННЯ', 'ОБЄДНАННЯ', 'ВАЛЮТА',
                                              'КУРС'])
    writer.writeheader()


    end_date = datetime.today()
    start_date = end_date - timedelta(days=90)
    current_date = start_date

    while current_date <= end_date:
        formatted_date = current_date.strftime("%d.%m.%Y")
        url = f'https://bank.gov.ua/ua/markets/exchangerates?date={formatted_date}'
        driver.get(url)

        time.sleep(2)


        table = driver.find_element(By.ID, 'exchangeRates')


        exchange_rates = []


        rows = table.find_elements(By.TAG_NAME, 'tr')[1:]
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')

            rate = {
                'ДАТА': formatted_date,
                'КОД': cells[0].text.strip(),
                'ПОЗНАЧЕННЯ': cells[1].text.strip(),
                'ОБЄДНАННЯ': cells[2].text.strip(),
                'ВАЛЮТА': cells[3].text.strip(),
                'КУРС': cells[4].text.strip()
            }
            # Додаємо дані до списку
            exchange_rates.append(rate)

        # Записуємо дані у CSV-файл
        writer.writerows(exchange_rates)

        # Перехід до наступного дня
        current_date += timedelta(days=1)

driver.quit()

print(f'Data has been written to {csv_filename}')
