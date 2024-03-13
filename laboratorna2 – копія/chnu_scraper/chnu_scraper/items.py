import scrapy

class FacultyItem(scrapy.Item):
    faculty_name = scrapy.Field()
    faculty_url = scrapy.Field()

class DepartmentItem(scrapy.Item):
    department_name = scrapy.Field()
    department_url = scrapy.Field()

class StaffItem(scrapy.Item):
    staff_name = scrapy.Field()

