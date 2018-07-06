# -*- coding: utf-8 -*-
import scrapy,re
from scrapy.selector import Selector
from picture_crawl import items


class HupuCrawlSpider(scrapy.Spider):
    '''
    爬取虎扑上jamse扣篮gif链接
    '''
    name = "hupu_crawl"
    allowed_domains = ["hupu.com"]
    start_urls = ['']
    spider_path = 'D:/idea-workspace/picture_crawl/'

    def __init__(self):
        self.start_urls = ['https://bbs.hupu.com/18520829.html']

    def parse(self, response):
        text = self.save_response(response)
        gifs = re.findall('data-url=(.*?.gif)',text,re.M)
        for i in range(len(gifs)):
            gifs[i] = gifs[i][1:]
        pictureItem = items.PictureCrawlItem()
        pictureItem['image_url'] = gifs
        with open(self.spider_path + "url",'w') as fw:
            fw.write("\n".join(gifs))
        fw.close()
        return pictureItem

    def save_response(self, response):
        with open(self.spider_path + "test",'w') as fw:
            fw.write(response.body)
        fw.close()
        text = open(self.spider_path + "test").read().replace('\t', '').replace('\n', '').replace(' ', '')
        return text
