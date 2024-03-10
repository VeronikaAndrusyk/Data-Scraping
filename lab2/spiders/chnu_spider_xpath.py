import scrapy
from lab2.lab2.items import FacultyItem, DepartmentItem, StaffItem

class ChnuSpiderXpath(scrapy.Spider):
    name = "chnu_xpath"
    allowed_domains = ["chnu.edu.ua"]
    start_urls = ["https://www.chnu.edu.ua/universytet/zahalni-vidomosti/fakultety-ta-instytuty/"]

    def parse(self, response):
        for td in response.xpath('//table[@class="table table-hover"]/tbody/tr/td'):
            link = td.xpath('.//a')
            if link:
                fac_name = link.xpath('./text()').get().strip()
                fac_link = link.xpath('./@href').get()

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
        for department_a_tag in response.xpath('//a[contains(text(), "Кафедра")]'):
            department_name = department_a_tag.xpath('./text()').get().strip()
            department_link = department_a_tag.xpath('./@href').get()

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
        for staff_tag in response.xpath('//strong'):
            if staff_tag.xpath('.//img'):
                staff_name = staff_tag.xpath('./text()').get().strip()

                yield StaffItem(
                    name=staff_name,
                    department=response.meta.get("department")
                )
