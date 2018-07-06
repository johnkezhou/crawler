# -*- coding: utf-8 -*-
import scrapy
from scrapy import log
from dianping_crawler import items
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class CommentSpiderSpider(scrapy.Spider):
    name = "comment_spider"
    allowed_domains = ["dianping.com"]
    start_urls = ['http://www.dianping.com/ajax/json/shopDynamic/allReview?shopId=10341887&cityId=3&categoryURLName=food&power=5&cityEnName=hangzhou&shopType=10']
    spider_path = 'D:/idea-workspace/dianping_crawler/'


    def parse(self, response):
        # self.save_response(response)
        # try:
        #     self.save_crawled_urls.write(response.url + "\n")
        # except Exception as e:
        #     self.log("save_crawled_urls error: " + str(e), level=log.ERROR)
        #     print e
        # self.delay(response.url)
        return self.build_items()
        pass


    def __init__(self):
        # crawling_urls = open(self.spider_path + 'review_urls').read().split("\n")
        # crawled_urls = open(self.spider_path + 'crawled_urls').read().split("\n")
        # self.start_urls = list(set(crawling_urls).difference(set(crawled_urls)))
        # self.save_review_file = open(self.spider_path + 'reviews_result', 'a+')
        # self.save_crawled_urls = open(self.spider_path + 'crawled_urls', 'a+')
        self.index = 0

    def save_response(self, response):
        try:
            self.save_review_file.write(response.body + "\n")
        except Exception as e:
            self.log("save_review_file error: " + str(e), level=log.ERROR)
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
        review_items = []
        # text = open(self.spider_path + "review_result").read().split("\n")
        text = open(self.spider_path + "reviews_result").readlines()
        print len(text)
        for tx in text:
            try:
                data = eval(tx.replace('true','True').replace('false','False').replace('null','""'))
                reviewlist = data['reviewAllDOList']
                for review in reviewlist:
                    try:
                        rvw = review['reviewDataVO']
                        item = items.Review()
                        for key in item.fields.keys():
                            fkey = self.filter_key(key)
                            if fkey in rvw.keys():
                                if fkey == 'star':
                                    value = "%s;%s" % (rvw[fkey]['value'], rvw[fkey]['desc'])
                                    pass
                                else:
                                    value = rvw[fkey]
                            else:
                                value = ''
                            item.__setitem__(key, value)
                        if 'scoreList' in rvw and isinstance(rvw['scoreList'], list):
                            score = rvw['scoreList']
                            for each in score:
                                if isinstance(each, dict) and 'value' in each:
                                    if each['title'] == '口味':
                                        item.__setitem__('taste_score', each['value'])
                                    if each['title'] == '环境':
                                        item.__setitem__('environment_score', each['value'])
                                    if each['title'] == '服务':
                                        item.__setitem__('service_score', each['value'])
                        if 'reviewData' in rvw:
                            rvdata = rvw['reviewData']
                            if isinstance(rvdata, dict) and 'clientType' in rvdata:
                                item.__setitem__('client_type', rvdata['clientType'])
                        review_items.append(item)
                    except Exception as e:
                        print "item", e
            except Exception as e:
                print "text", e
        return review_items

