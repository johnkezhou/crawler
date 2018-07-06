# -*- coding: utf-8 -*-
import scrapy
from scrapy import log
from dianping_crawler import items
import time
from scrapy.selector import Selector
import xmltodict
from xml.etree.ElementTree import Element, tostring, parse
import re,os
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class UserDetailSpiderSpider(scrapy.Spider):
    name = "user_detail_spider"
    allowed_domains = ["dianping.com"]
    start_urls = ['http://www.dianping.com/member/48910910']
    spider_path = 'D:/idea-workspace/dianping_crawler/'

    def __init__(self):
        crawling_urls = open(self.spider_path + 'user_urls').read().split("\n")
        crawled_urls = open(self.spider_path + 'crawled_urls').read().split("\n")
        self.start_urls = list(set(crawling_urls).difference(set(crawled_urls)))
        self.save_crawled_urls = open(self.spider_path + 'crawled_urls', 'a+')
        self.start_urls = ['http://www.dianping.com/member/48910910']
        self.xpath = self.get_xpath()
        self.index = 0
        self.person_info_re = {'birth':'生日：</em>(.*?)</li>',
                               'love_state':'恋爱状态：</em>(.*?)</li>',
                               'constellation':'星座：</em>(.*?)</li>',
                               'hobby':'体型：</em>(.*?)</li>',
                               'food_type':'生日：</em>(.*?)</li>'}

    def parse(self, response):
        # self.save_crawled_urls.write(response.url+"\n")
        self.save_response(response)
        # self.delay(response.url)
        self.get_member_files()

    def get_member_files(self):
        path = self.spider_path + "member"
        filelist = os.listdir(path)
        user_items = []
        filelist = ['48910910']
        for filename in filelist:
            filepath = os.path.join(path, filename)
            text = open(filepath).read()
            user_items.append(self.get_detail_item(text, filename))
        return user_items


    def get_detail_item(self, text, user_id):
        select = Selector(text=text)
        user_item = items.User()
        keys = user_item.fields.keys()
        for key in keys:
            if key in self.xpath :
                value = self.select_value(self.xpath[key], select)
                print key, value
                user_item.__setitem__(key, value)
            if key == 'mana_score':
                self.find_mana_score(user_item.__getitem__(key), user_item)
        user_item.__setitem__('user_id', user_id)
        print user_item
        return user_item


    def get_relations(self, text, user_id):
        select = Selector(text=text)
        follows = select.xpath('/html/body/div[2]/div[2]/div/div[1]/div[2]/div[2]/div[1]/ul').extract()
        relations = []
        for i in range(len(follows)):
            select = Selector(text=follows[i])
            fw_id = select.xpath('//li[%s]/a/img/@user-id'%(i+1)).extract()
            fw_pic = select.xpath('//li[%s]/a/img/@src'%(i+1)).extract()
            fw_name = select.xpath('//li[%s]/p/a/text()'%(i+1)).extract()
            print fw_id, fw_name, fw_pic
            relations.append((user_id, fw_id, fw_name, fw_pic))
        print relations
        return relations

    def get_personal_info(self, item):
        text = item.__getitem__('birth')

    def find_mana_score(self, text, item):
        try:
            tmp = re.findall('J_col_exp">(.*?)<i', text)
            item.__setitem__('mana_score', int(tmp[0]))
        except Exception as e:
            self.log("find_mana_score: " + str(e), level=log.ERROR)
            print e

    def get_xpath(self):
        try:
            tree = parse(self.spider_path + 'xpath.xml')
            string = tostring(tree.getroot())
            edt = xmltodict.parse(string)
            return edt['xpath']['user_item']
        except Exception as e:
            self.log("get_xpath: " + str(e), level=log.ERROR)
            print e

    def save_response(self, response):
        try:
            user_id = response.url.split("/")[-1]
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

    def select_value(self, xpath, select):
        try:
            if xpath == '' or xpath == None:
                return ''
            value = select.xpath(xpath).extract()
            if len(value) > 0:
                value = value[0]
            else:
                value = ''
            if value.find("</p>") != -1:
                tmp = self.re_find('</span>(.*?)</p>', value)
                if tmp:
                    value = tmp
            return value
        except Exception as e:
            self.log("xpath error: " + str(e), level=log.ERROR)
            print e
            return None

    def re_find(self, pattern, text):
        try:
            tmp = re.findall(pattern, text, re.M)
            if tmp[0]:
                return tmp[0]
        except Exception as e:
            self.log("re error: " + str(e), level=log.ERROR)
            return None