# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline

class PictureCrawlPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_url']:
            yield scrapy.Request(image_url)


    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise  DropItem("Item contains no images")
        item['images'] = image_path
        return item
