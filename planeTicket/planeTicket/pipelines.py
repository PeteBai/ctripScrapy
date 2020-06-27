# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from . import settings
from scrapy.exporters import JsonLinesItemExporter
import datetime
#import settings

class PlaneticketPipeline:
    def __init__(self):
        today=str(datetime.date.today())
        self.file = open(today+".txt","ab+")
        self.jsonLinesItemExporter = JsonLinesItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
    
    def close_spider(self,spider):
            spider.logger.info("saving data file...")
            self.file.close()
  
    def process_item(self, item, spider=None):
        self.jsonLinesItemExporter.export_item(item)
        return item


