# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib.request import urlretrieve

# useful for handling different item types with a single interface

from la2.items import FacultyItem, DepartmentItem

class UpperCasePipeline:
    def process_item(self, item, spider):
        if isinstance(item, FacultyItem):
            item['name'] = item['name'].upper()
        elif isinstance(item, DepartmentItem):
            item['name'] = item['name'].upper()
        return item

class NumberingPipeline:
    def __init__(self):
        self.departments_count = {}

    def process_item(self, item, spider):
        if isinstance(item, DepartmentItem):
            faculty_name = item.get('faculty')
            if faculty_name not in self.departments_count:
                self.departments_count[faculty_name] = 1
            else:
                self.departments_count[faculty_name] += 1
            item['name'] = f"{self.departments_count[faculty_name]}. {item['name']}"
        return item





