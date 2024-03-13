import scrapy
import csv
import json
from bs4 import BeautifulSoup
from chnu_scraper.items import FacultyItem, DepartmentItem, StaffItem
from scrapy.exporters import XmlItemExporter


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
                        department_name = response.meta.get("department")

                        # CSV file
                        with open('chnu_data.csv', mode='a', newline='', encoding='utf-8') as csv_file:
                            writer = csv.writer(csv_file)
                            writer.writerow([department_name, staff_name])

                        #  JSON file
                        with open('chnu_data.json', mode='a', encoding='utf-8') as json_file:
                            json.dump({"department": department_name, "staff_name": staff_name}, json_file)
                            json_file.write('\n')

                        #  XML file
                        with open('chnu_data.xml', mode='ab') as xml_file:
                            exporter = XmlItemExporter(xml_file)
                            exporter.start_exporting()
                            exporter.export_item({"department": department_name, "staff_name": staff_name})
                            exporter.finish_exporting()

        except Exception as e:
            self.logger.error("Error occurred while parsing: %s", str(e))
