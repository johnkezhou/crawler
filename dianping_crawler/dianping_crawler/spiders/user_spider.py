# -*- coding: utf-8 -*-
import scrapy
from scrapy import log
from dianping_crawler import items
import time
import xmltodict
from xml.etree.ElementTree import Element, tostring, parse
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class UserSpiderSpider(scrapy.Spider):
    name = "user_spider"
    allowed_domains = ["dianping.com"]
    start_urls = ['http://www.dianping.com/member/48910910']
    spider_path = 'D:/idea-workspace/dianping_crawler/'

    def __init__(self):
        # crawling_urls = open(self.spider_path + 'review_urls').read().split("\n")
        # crawled_urls = open(self.spider_path + 'crawled_urls').read().split("\n")
        # self.start_urls = list(set(crawling_urls).difference(set(crawled_urls)))
        # self.save_crawled_urls = open(self.spider_path + 'crawled_urls', 'a+')
        self.index = 0

    def parse(self, response):
        self.save_response(response)
        # try:
        #     self.save_crawled_urls.write(response.url + "\n")
        # except Exception as e:
        #     self.log("save_crawled_urls error: " + str(e), level=log.ERROR)
        #     print e
        # self.delay(response.url)

        pass

    def save_response(self, response):
        user_id = response.url.split("/")[-1]
        try:
            path = self.spider_path + 'member/%s' % user_id
            with open(path,'w') as fw:
                fw.write(response.body)
            fw.close()
        except Exception as e:
            self.log("write text: " + str(e), level=log.ERROR)
            print e

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
        self.index += 1

    def transform_key(self, key):
        tmp = []
        for i in range(len(key)):
            if key[i] >= 'A' and key[i] <= 'Z':
                tmp.append("_%s" % key[i].lower())
            else:
                tmp.append(key[i])
        return "".join(tmp)

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

    def build_items(self):
        user_items = []
        # text = open(self.spider_path + "review.json").readlines()
        text = open(self.spider_path + "reviews_result").readlines()
        for tx in text:
            try:
                data = eval(tx.replace('true','True').replace('false','False').replace('null','""'))
                reviewlist = data['reviewAllDOList']
                for review in reviewlist:
                    try:
                        userv = review['user']
                        item = items.User()
                        for key in item.fields.keys():
                            fkey = self.filter_key(key)
                            if fkey in userv and userv[fkey] != '':
                                value = userv[fkey]
                            else:
                                value = ''
                            item.__setitem__(key, value)
                        if 'vipLevel' in review:
                            item.__setitem__('vip_level', review['vipLevel'])
                        if 'userLevelTitle' in review:
                            item.__setitem__('user_level_title', review['userLevelTitle'])
                        user_items.append(item)
                    except Exception as e:
                        print "item", e
            except Exception as e:
                print "text", e
        return list(set(user_items))