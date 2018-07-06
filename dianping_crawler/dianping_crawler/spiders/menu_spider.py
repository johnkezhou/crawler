# -*- coding: utf-8 -*-
import scrapy
from scrapy import log
import time
from dianping_crawler import items
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class MenuSpiderSpider(scrapy.Spider):
    name = "menu_spider"
    allowed_domains = ["dianping.com"]
    start_urls = []
    url_header = 'http://www.dianping.com/'
    spider_path = 'D:/idea-workspace/dianping_crawler/'

    def __init__(self):
        crawling_urls = open(self.spider_path + 'menu_urls_50').read().split("\n")
        crawled_urls = open(self.spider_path + 'crawled_urls').read().split("\n")
        self.start_urls = list(set(crawling_urls).difference(set(crawled_urls)))
        self.save_menu_file = open(self.spider_path + 'menu_tab', 'a+')
        self.save_crawled_urls = open(self.spider_path + 'crawled_urls', 'a+')
        self.index = 0

    def delay(self, url):
        '''
        延时方法
        :param url:
        :return:
        '''
        print url, self.index, len(self.start_urls)
        if self.index % 35 == 0 and self.index != 0:
            time.sleep(120)
        self.index += 1

    def parse(self, response):
        try:
            self.save_crawled_urls.write(response.url + "\n")
        except Exception as e:
            self.log("save_crawled_urls error: " + str(e), level=log.ERROR)
            print e
        self.delay(response.url)
        self.save_response(response)
        return self.parse_item(response.body)

    def save_response(self, response):
        text = response.body
        self.save_menu_file.write(text + "\n")

    def parse_item(self, text):
        menu_tab = {}
        text = text.replace('null','""').replace('true','True').replace('false','False')
        all_dish = []
        try:
            menu_tab = eval(text)
            all_dish = menu_tab['allDishes']
        except Exception as e:
            self.log("menu transform error: " + str(e), level=log.ERROR)
        dish_list = []
        for dish in all_dish:
            dh = self.get_item(dish)
            dish_list.append(dh)
        print "dish_list: ", len(dish_list)
        return dish_list


    def get_item(self, dish_dict):
        dish_item = items.Dish()
        for key in dish_item.fields.keys():
            fkey = self.filter_key(key)
            if fkey in dish_dict.keys():
                value = dish_dict[fkey]
            else:
                value = ''
            dish_item.__setitem__(key, value)
        return dish_item

    def filter_key(self, key):
        '''
        将下划线字段转换为驼峰型字段
        :param key:
        :return:
        '''
        tmp = key.split('_')
        for i in range(1, len(tmp)):
            tmp[i] = tmp[i][0].upper() + tmp[i][1:]
        return ''.join(tmp)

