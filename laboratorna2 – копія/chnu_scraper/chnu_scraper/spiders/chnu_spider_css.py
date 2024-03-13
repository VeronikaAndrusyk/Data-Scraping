import scrapy
import csv
from chnu_scraper.items import FacultyItem, DepartmentItem, StaffItem


class ChnuSpider(scrapy.Spider):
    name = 'chnu_spider_css'
    start_urls = ['https://www.chnu.edu.ua/universytet/zahalni-vidomosti/fakultety-ta-instytuty/']

    def parse(self, response):
        for faculty_link in response.css('table.table.table-hover td a'):
            faculty_name = faculty_link.css('::text').get().strip()
            faculty_url = faculty_link.css('::attr(href)').get()

            # екземпляр об'єкту FacultyItem та передаємо в нього зібрані дані
            faculty_item = FacultyItem()
            faculty_item['faculty_name'] = faculty_name
            faculty_item['faculty_url'] = faculty_url
            yield faculty_item

            yield response.follow(faculty_url, callback=self.parse_department)

    def parse_department(self, response):
        for department_link in response.css('a::text').re(r'Кафедра.*'):
            department_name = department_link.strip()
            department_url = response.urljoin(response.css('a::attr(href)').get())

            # екземпляр об'єкту DepartmentItem та передаємо в нього зібрані дані
            department_item = DepartmentItem()
            department_item['department_name'] = department_name
            department_item['department_url'] = department_url
            yield department_item

            yield response.follow(department_url, callback=self.parse_staff)

    def parse_staff(self, response):
        for staff_name in response.css('strong img+text::text').getall():
            # Створюємо екземпляр об'єкту StaffItem та передаємо в нього зібрані дані
            staff_item = StaffItem()
            staff_item['staff_name'] = staff_name.strip()
            yield staff_item

            # дані до CSV-файлу
            with open('chnu_data.csv', mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([response.meta.get("department"), staff_name.strip()])
