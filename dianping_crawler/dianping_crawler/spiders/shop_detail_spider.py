# -*- coding: utf-8 -*-
import scrapy
import re, json
import random
from scrapy.selector import Selector
from scrapy import log
import os
import time
from dianping_crawler import items
from xml.etree.ElementTree import Element, tostring, parse
import xmltodict

class ShopDetailSpiderSpider(scrapy.Spider):
    name = "shop_detail_spider"
    allowed_domains = ["dianping.com"]
    start_urls = ['http://dianping.com/']
    spider_path = 'D:/idea-workspace/dianping_crawler/'
    menu_url_header = 'http://www.dianping.com/ajax/json/shopDynamic/shopTabs?'
    review_url_header = 'http://www.dianping.com/ajax/json/shopDynamic/allReview?'
    menu_conditions = ['shopId', 'cityId', 'shopName', 'power', 'mainCategoryId', 'shopType', 'shopCityId']

    def parse(self, response):
        try:
            self.save_crawled_urls.write(response.url + "\n")
        except Exception as e:
            self.log("save_crawled_urls error: " + str(e), level=log.ERROR)
            print e
        self.delay(response.url)
        self.save_response(response)
        shop_config = self.get_shop_config(response.body)
        self.build_menu_url(shop_config)
        return self.get_item(shop_config)


    def delay(self, url):
        '''
        延时方法
        :param url:
        :return:
        '''
        index = self.start_urls.index(url)
        print url, index, len(self.start_urls)
        if index % 35 == 0 and index != 0:
            time.sleep(120)


    def __init__(self):
        '''
        初始化爬虫程序
        '''
        crawling_urls = open(self.spider_path + 'shop_urls').read().split("\n")
        crawled_urls = open(self.spider_path + 'crawled_urls').read().split("\n")
        self.start_urls = list(set(crawling_urls).difference(set(crawled_urls)))
        self.xpath = self.get_xpath()
        self.shop_detail_file = open(self.spider_path + "pipeline_shopconfig",'a+')
        self.menu_url_file = open(self.spider_path + "menu_urls", 'a+')
        self.save_crawled_urls = open(self.spider_path + 'crawled_urls', 'a+')

    def save_response(self, response):
        '''
        保存爬取的html页面
        :param response:
        :return:
        '''
        text = response.body
        file_name = response.url.split("/")[-1]
        with open(self.spider_path + "shop/" + file_name, 'wb') as fw:
            fw.write(text)
        fw.close()

    def get_shop_config(self, text):
        '''
        获取shop_config字典项
        :param text: html页面
        :return: shop_config字典项
        '''
        data = text.replace('\t', '').replace('\n', '').replace(' ', '')
        shop_config = {}
        try:
            sc = re.findall('<script>window.shop_config=(.*?)</script>', data, re.M)
            sc = sc[0].replace('{','{"').replace(':','":').replace(',',',"').replace('"://','://')
            shop_config = eval(sc)
        except Exception as e:
            self.log("shop config: " + str(e), level=log.ERROR)
        try:
            select = Selector(text=text)
            tmp = select.xpath(self.xpath['shop_info']).extract()
            shop_config['shopInfo'] = ''.join(tmp).replace('\t', '').replace('\n', '').replace(' ', '')
        except Exception as e:
            self.log("shop_info: " + str(e), level=log.ERROR)
        try:
            select = Selector(text=text)
            tmp = select.xpath(self.xpath['opening_time']).extract()
            shop_config['openingTime'] = ''.join(tmp).replace('\t', '').replace('\n', '').replace(' ', '')
        except Exception as e:
            self.log("opening_time: " + str(e), level=log.ERROR)
        self.shop_detail_file.write(json.dumps(shop_config) + "\n")
        return shop_config

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

    def build_menu_url(self, shop_config):
        '''
        组装字段创建menu_url
        :param shop_config:
        :return:
        '''
        condition = []
        for cd in self.menu_conditions:
            condition.append('%s=%s'%(cd, shop_config[cd]))
        url = self.menu_url_header + "&".join(condition)
        self.menu_url_file.write(url+"\n")

    def get_item(self, shop_config):
        shop_item = items.Shop()
        for key in shop_item.fields.keys():
            fkey = self.filter_key(key)
            if fkey in shop_config.keys():
                value = shop_config[fkey]
            else:
                value = ''
            shop_item.__setitem__(key, value)
        return shop_item

    def get_xpath(self):
        '''
        读取xpath.xml文件
        :return:
        '''
        tree = parse(self.spider_path + 'xpath.xml')
        string = tostring(tree.getroot())
        edt = xmltodict.parse(string)
        return edt['shop_item']