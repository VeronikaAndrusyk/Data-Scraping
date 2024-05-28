import scrapy
from bs4 import BeautifulSoup
import requests
from la2.items import FacultyItem, DepartmentItem

class ChnuSpider(scrapy.Spider):
    name = "chnu"
    allowed_domains = ["chnu.edu.ua"]
    start_urls = ["https://www.chnu.edu.ua/universytet/zahalni-vidomosti/fakultety-ta-instytuty/"]

    api_url = "http://localhost:3000/api"  # Адреса вашого API

    def parse(self, response):
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            fac_list = soup.find("table", class_="table table-hover")

            if fac_list:
                for tr in fac_list.find_all("tr"):
                    img_td = tr.find("td", valign="middle", width="120")
                    if img_td:
                        img_url = img_td.find("img").get("src")
                        fac_name = tr.find("strong").text.strip()
                        fac_link = tr.find("a").get("href")

                        # Відправка даних факультету на API
                        faculty_data = {
                            'name': fac_name,
                            'image': response.urljoin(img_url),
                            'link': fac_link
                        }
                        requests.post(f"{self.api_url}/faculties", json=faculty_data)

                        yield scrapy.Request(
                            url=fac_link,
                            callback=self.parse_faculty,
                            meta={"faculty": fac_name}
                        )
        except Exception as e:
            self.logger.error("Error occurred while parsing: %s", str(e))

    def parse_faculty(self, response):
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            department_a_tags = soup.find_all("a", string=lambda text: text and "Кафедра" in text)

            if department_a_tags:
                for department_a_tag in department_a_tags:
                    department_name = department_a_tag.text.strip()

                    # Відправка даних кафедри на API
                    department_data = {
                        'name': department_name,
                        'faculty': response.meta.get("faculty")
                    }
                    requests.post(f"{self.api_url}/departments", json=department_data)

                    yield DepartmentItem(
                        name=department_name,
                        faculty=response.meta.get("faculty")
                    )
        except Exception as e:
            self.logger.error("Error occurred while parsing: %s", str(e))
