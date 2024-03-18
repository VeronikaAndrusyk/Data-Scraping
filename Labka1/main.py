from requests import get
from bs4 import BeautifulSoup
import re

BASE_URL = "https://www.chnu.edu.ua"
URL = f"{BASE_URL}/universytet/zahalni-vidomosti/fakultety-ta-instytuty/"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
page = get(URL, headers=HEADERS)
soup = BeautifulSoup(page.content, "html.parser")

fac_list = soup.find("table", class_="table table-hover")

FILE_NAME = "chnu.txt"
with open(FILE_NAME, "w", encoding="utf-8") as file:
    for td in fac_list.find_all("td"):
        link = td.find("a")
        if link is not None:
            fac_name = link.text.strip()
            fac_link = link.get("href")
            file.write(f"Назва факультету: {fac_name}\n")
            file.write(f"URL: {fac_link}\n")

            print(f"Назва факультету: {fac_name}")
            print(f"URL: {fac_link}")

            # доступ до кожної сторінки факультету для пошуку кафедр
            faculty_page = get(fac_link)
            faculty_soup = BeautifulSoup(faculty_page.content, "html.parser")

            # знаходження і вивід посилання кафедри
            department_a_tags = faculty_soup.find_all("a", string=lambda text: text and "Кафедра" in text)

            for department_a_tag in department_a_tags:
                department_name = department_a_tag.text.strip()
                department_link = department_a_tag.get("href")
                file.write(f"    Кафедра: {department_name}\n")
                file.write(f"    URL кафедри: {department_link}\n")
                print(f"    Кафедра: {department_name}")
                print(f"    URL кафедри: {department_link}")

                # доступ до сторінки кафедри для пошуку працівників
                department_page = get(department_link)
                department_soup = BeautifulSoup(department_page.content, "html.parser")

                # Змінений регулярний вираз для вибору імен працівників
                staff_tags = department_soup.find_all(
                    lambda tag: tag.name == 'strong' and re.match(r'^[\w\s\.\-]+$', tag.text.strip()))

                # Створення множини для зберігання унікальних імен працівників
                unique_staff_names = set()

                for staff_tag in staff_tags:
                    staff_name = staff_tag.text.strip()
                    # Перевірка, чи ім'я ще не було додане до множини
                    if staff_name not in unique_staff_names:
                        file.write(f"        Staff Name: {staff_name}\n")
                        print(f"        Staff Name: {staff_name}")
                        # Додавання імені до множини
                        unique_staff_names.add(staff_name)