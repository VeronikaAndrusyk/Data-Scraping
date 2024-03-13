import scrapy
import xml.etree.ElementTree as ET

class ChnuSpider(scrapy.Spider):
    name = 'chnu_spider_xpath'
    start_urls = ['https://www.chnu.edu.ua/universytet/zahalni-vidomosti/fakultety-ta-instytuty/']

    def parse(self, response):
        faculties = ET.Element('faculties')

        for faculty_link in response.xpath('//table[@class="table table-hover"]//td/a'):
            faculty_name = faculty_link.xpath('string()').get().strip()
            faculty_url = faculty_link.xpath('@href').get()

            faculty_element = ET.SubElement(faculties, 'faculty')
            ET.SubElement(faculty_element, 'name').text = faculty_name
            ET.SubElement(faculty_element, 'url').text = faculty_url

            yield response.follow(faculty_url, callback=self.parse_department)

        tree = ET.ElementTree(faculties)
        tree.write('faculties.xml', encoding='utf-8', xml_declaration=True)

    def parse_department(self, response):
        departments = ET.Element('departments')

        for department_link in response.xpath('//a[contains(text(), "Кафедра")]'):
            department_name = department_link.xpath('text()').get().strip()
            department_url = response.urljoin(department_link.xpath('@href').get())

            department_element = ET.SubElement(departments, 'department')
            ET.SubElement(department_element, 'name').text = department_name
            ET.SubElement(department_element, 'url').text = department_url

            yield response.follow(department_url, callback=self.parse_staff)

        tree = ET.ElementTree(departments)
        tree.write('departments.xml', encoding='utf-8', xml_declaration=True)

    def parse_staff(self, response):
        staffs = ET.Element('staffs')

        for staff_name in response.xpath('//strong/following-sibling::text()').getall():
            staff_element = ET.SubElement(staffs, 'staff')
            ET.SubElement(staff_element, 'name').text = staff_name.strip()

        tree = ET.ElementTree(staffs)
        tree.write('staffs.xml', encoding='utf-8', xml_declaration=True)
