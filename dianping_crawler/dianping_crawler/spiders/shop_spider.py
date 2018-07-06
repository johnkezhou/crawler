# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import random
from scrapy import log
import os
import time
from dianping_crawler import items
import xmltodict
from xml.etree.ElementTree import Element, tostring, parse
import re


class ShopSpiderSpider(scrapy.Spider):
    name = "shop_spider"
    allowed_domains = ["dianping.com"]
    start_urls = []
    url_header = 'http://www.dianping.com/search/category/3/10/'
    xpath = {}
    spider_path = 'D:/idea-workspace/dianping_crawler/'

    def __init__(self):
        crawling_urls = open(self.spider_path + 'crawling_urls').read().split("\n")
        crawled_urls = open(self.spider_path + 'crawled_urls').read().split("\n")
        self.start_urls = list(set(crawling_urls).difference(set(crawled_urls)))
        self.save_crawled_urls = open(self.spider_path + 'crawled_urls', 'a+')
        self.xpath = self.get_xpath()

    def get_dir_file(self, url):
        is_dir = True
        if url.find('p') != -1:
            is_dir = False
        tmp = url.split("/")
        p = tmp[-1].index('p')
        return is_dir, tmp[-1][:p], tmp[-1][p:]

    def save_response(self, response):
        text = response.body
        is_dir, dir, file = self.get_dir_file(response.url)
        print is_dir, dir, file
        if is_dir:
            try:
                path = self.spider_path + 'location_foodType/%s/' % dir
                self.append_urls(text, response.url)
                if not os.path.exists(path):
                    os.makedirs(path)
            except Exception as e:
                self.log("create dir: " + str(e), level=log.ERROR)
                print e
                return
            try:
                with open(path + "p1", 'w') as fw:
                    self.log(path + "p1", level=log.INFO)
                    fw.write(text)
            except Exception as e:
                self.log("create dir: " + str(e), level=log.ERROR)
                print e
        else:
            try:
                with open(self.spider_path + "location_foodType/%s/%s" % (dir, file), 'w') as fw:
                    fw.write(text)
                    self.log(self.spider_path + "location_foodType/%s/%s" % (dir, file), level=log.INFO)
            except Exception as e:
                self.log("create dir: " + str(e), level=log.ERROR)
                print e

    def delay(self, url):
        index = self.start_urls.index(url)
        print url, index
        if index % 35 == 0 and index != 0:
            time.sleep(120)

    def get_items(self, text):
        shop_list = None
        with open(self.spider_path + "test", 'w') as fw:
            fw.write(text)
        text = open(self.spider_path + "test").read()
        try:
            select = Selector(text=text)
            shop_list = select.xpath('//*[@id="shop-all-list"]/ul//li').extract()
        except Exception as e:
            self.log("shop_list : " + str(e), level=log.ERROR)
            print e
        shop_items = []
        shop_urls = []
        if shop_list is None:
            return shop_items, shop_urls
        for shop in shop_list:
            try:
                select = Selector(text=shop)
                shop_item = items.Shop()
                keys = shop_item.fields.keys()
                for key in keys:
                    value = self.select_value(self.xpath[key], select)
                    shop_item.__setitem__(key, value)
                shop_item.__setitem__('shop_id', shop_item.__getitem__('shop_url').split("/")[-1])
                shop_items.append(shop_item)
                shop_urls.append(shop_item.__getitem__('shop_url'))
            except Exception as e:
                self.log("shop item : " + str(e), level=log.ERROR)
                print e
        return shop_items, shop_urls

    def select_value(self, xpath, select):
        try:
            if xpath == '' or xpath == None:
                return ''
            value = select.xpath(xpath).extract()
            if len(value) > 0:
                value = value[0]
            else:
                value = ''
            return value
        except Exception as e:
            self.log("xpath error: " + str(e), level=log.ERROR)
            print e
            return None

    def get_xpath(self):
        tree = parse(self.spider_path + 'xpath.xml')
        string = tostring(tree.getroot())
        edt = xmltodict.parse(string)
        return edt['shop_item']

    def parse(self, response):
        try:
            self.save_crawled_urls.write(response.url + "\n")
        except Exception as e:
            self.log("save_crawled_urls error: " + str(e), level=log.ERROR)
            print e
        self.delay(response.url)
        self.log(response.url, level=log.INFO)
        self.save_response(response)
        shop_items = []
        shop_urls = []
        shop_items, shop_urls = self.get_items(response.body)
        try:
            with open(self.spider_path + "shop_urls", 'a+') as fw:
                fw.write("\n".join(shop_urls) + "\n")
            fw.close()
        except Exception as e:
            self.log("shop_urls error: " + str(e), level=log.ERROR)
        return shop_items

    def append_urls(self, text, url):
        try:
            page = re.findall('data-ga-page', text, re.M)
            url_list = []
            if page is not None:
                page_list = range(2, len(page))
                random.shuffle(page_list)
                for pl in page_list:
                    url_list.append(url + "p%s" % pl)
            if len(url_list) == 0:
                return
            with open('D:/idea-workspace/dianping_crawler/beyond_p1', 'a+') as fw:
                fw.write("\n".join(url_list) + "\n")
        except Exception as e:
            self.log("shop-page error: " + str(e), level=log.ERROR)
            print e

    def get_init_data(self):
        root_dir = self.spider_path + "location_foodType"
        allfile = []
        allfile = self.dirlist(root_dir, allfile)
        shop_items = []
        for file in allfile:
            text = open(file).read()
            shops, url = self.get_items(text)
            shop_items.extend(shops)
        return shop_items, []

    def dirlist(self, path, allfile):
        filelist = os.listdir(path)
        for filename in filelist:
            filepath = os.path.join(path, filename)
            if os.path.isdir(filepath):
                child_filelist = os.listdir(filepath)
                for cf in child_filelist:
                    allfile.append(os.path.join(filepath, cf))
            else:
                allfile.append(filepath)
        return allfile
