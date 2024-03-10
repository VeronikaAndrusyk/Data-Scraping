import scrapy
from bs4 import BeautifulSoup
from lab2.lab2.items import FacultyItem, DepartmentItem, StaffItem


class ChnuSpider(scrapy.Spider):
    name = "chnu"
    allowed_domains = ["chnu.edu.ua"]
    start_urls = ["https://www.chnu.edu.ua/universytet/zahalni-vidomosti/fakultety-ta-instytuty/"]

    def parse(self, response):
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            fac_list = soup.find("table", class_="table table-hover")

            if fac_list:
                for td in fac_list.find_all("td"):
                    link = td.find("a")
                    if link:
                        fac_name = link.text.strip()
                        fac_link = link.get("href")

                        yield FacultyItem(
                            name=fac_name,
                            url=fac_link
                        )

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
                    department_link = department_a_tag.get("href")

                    yield DepartmentItem(
                        name=department_name,
                        url=department_link,
                        faculty=response.meta.get("faculty")
                    )

                    yield scrapy.Request(
                        url=department_link,
                        callback=self.parse_department,
                        meta={"department": department_name}
                    )
        except Exception as e:
            self.logger.error("Error occurred while parsing: %s", str(e))

    def parse_department(self, response):
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            staff_tags = soup.find_all("strong")

            if staff_tags:
                for staff_tag in staff_tags:
                    if staff_tag.find("img"):
                        staff_name = staff_tag.text.strip()

                        yield StaffItem(
                            name=staff_name,
                            department=response.meta.get("department")
                        )
        except Exception as e:
            self.logger.error("Error occurred while parsing: %s", str(e))
