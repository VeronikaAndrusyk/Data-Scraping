import scrapy
from lab2.lab2.items import FacultyItem, DepartmentItem, StaffItem

class ChnuSpiderCss(scrapy.Spider):
    name = "chnu_css"
    allowed_domains = ["chnu.edu.ua"]
    start_urls = ["https://www.chnu.edu.ua/universytet/zahalni-vidomosti/fakultety-ta-instytuty/"]

    def parse(self, response):
        for td in response.css('table.table.table-hover td'):
            link = td.css('a')
            if link:
                fac_name = link.css('::text').get().strip()
                fac_link = link.css('::attr(href)').get()

                yield FacultyItem(
                    name=fac_name,
                    url=fac_link
                )

                yield scrapy.Request(
                    url=fac_link,
                    callback=self.parse_faculty,
                    meta={
                        "faculty": fac_name
                    }
                )

    def parse_faculty(self, response):
        for department_a_tag in response.css('a:contains("Кафедра")'):
            department_name = department_a_tag.css('::text').get().strip()
            department_link = department_a_tag.css('::attr(href)').get()

            yield DepartmentItem(
                name=department_name,
                url=department_link,
                faculty=response.meta.get("faculty")
            )

            yield scrapy.Request(
                url=department_link,
                callback=self.parse_department,
                meta={
                    "department": department_name
                }
            )

    def parse_department(self, response):
        for staff_tag in response.css('strong'):
            if staff_tag.css('img'):
                staff_name = staff_tag.css('::text').get().strip()

                yield StaffItem(
                    name=staff_name,
                    department=response.meta.get("department")
                )
