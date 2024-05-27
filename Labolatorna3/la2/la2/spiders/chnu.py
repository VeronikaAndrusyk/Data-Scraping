import scrapy
from bs4 import BeautifulSoup
import csv
from la2.items import FacultyItem, DepartmentItem

class ChnuSpider(scrapy.Spider):
    name = "chnu"
    allowed_domains = ["chnu.edu.ua"]
    start_urls = ["https://www.chnu.edu.ua/universytet/zahalni-vidomosti/fakultety-ta-instytuty/"]

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

                        print("Faculty:", fac_name)  # Print faculty name to console

                        # Write faculty data to CSV file
                        with open('faculty_data.csv', mode='a', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            writer.writerow([fac_name, response.urljoin(img_url), fac_link])

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

                    print("Department:", department_name)  # Print department name to console

                    yield DepartmentItem(
                        name=department_name,
                        faculty=response.meta.get("faculty")
                    )
        except Exception as e:
            self.logger.error("Error occurred while parsing: %s", str(e))
