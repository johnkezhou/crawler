# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import settings
import datetime
from scrapy import log
import json
from xml.etree.ElementTree import Element, tostring, parse
import xmltodict
import sys
reload(sys)
sys.setdefaultencoding('utf8')

notkyes=['shop_id', 'address', 'main_category_name']

class DianpingCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class FilePipeline(object):
    spider_path = 'D:/idea-workspace/dianping_crawler/'

    def process_item(self, item, spider):
        if spider.name == 'shop_spider':
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line)
        if spider.name == 'shop_detail_spider':
            pass
            # line = json.dumps(dict(item)) + "\n"
            # self.shopconfig_file.write(line)
        return item

    def __init__(self):
        self.file = open(self.spider_path + "pipeline_shop", 'a+')
        self.shopconfig_file = open(self.spider_path + "pipeline_shopconfig", 'a+')



class MySQLPipeline(object):

    def process_item(self, item, spider):
        if spider.name in self.base_spiders:
            sql = None
            try:
                sql = self.build_sql(item, self.base_spiders[spider.name])
            except Exception as e:
                log.msg(message="%s build sql: %s, error: " % (sql, spider.name) + str(e), _level=log.ERROR)
            if sql is None:
                return
            try:
                self.cursor.execute(sql)
                self.connect.commit()
            except Exception as e:
                log.msg(message="%s sql execute error: " % spider.name + str(e), _level=log.ERROR)
        elif spider.name in self.detail_spider:
            sql = None
            try:
                table_name = self.detail_spider[spider.name][0]
                primary_key = self.detail_spider[spider.name][1]
                sql = self.build_sql_shop_detail_spider(item, table_name, primary_key)
            except Exception as e:
                log.msg(message="%s build sql: %s, error: " % (sql, spider.name)  + str(e), _level=log.ERROR)
            if sql is None:
                return
            try:
                self.cursor.execute(sql)
                self.connect.commit()
            except Exception as e:
                log.msg(message="%s sql execute error: " % spider.name + str(e), _level=log.ERROR)

    def build_sql(self, item, table_name):
        data = dict(item)
        curTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = 'INSERT INTO %s (' % table_name
        keys = []
        values = []
        try:
            keys = data.keys()
            values = data.values()
        except Exception as e:
            print e
        keys.append('create_time')
        keys.append('operate_time')
        values.append(curTime)
        values.append(curTime)
        for i in range(len(values)):
            values[i] = '"' + str(values[i]) + '"'
        log.msg('keys length:%s, values length:%s' % (len(keys), len(values)), _level=log.INFO)
        sql += ",".join(keys) + ") VALUES(" + ",".join(values) + ");"
        log.msg('sql: %s' % (sql), _level=log.INFO)
        return sql

    spider_path = 'D:/idea-workspace/dianping_crawler/'

    def build_sql_shop_detail_spider(self, item, table_name, primary_key):
        data = dict(item)
        curTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updates = []
        for key, value in data.items():
            if key not in notkyes:
                if value != '':
                    updates.append('%s = "%s"' % (key, value))
        updates.append("operate_time = '%s'"%curTime)
        fix = " , ".join(updates)
        sql = 'UPDATE %s SET %s WHERE %s = %s;' %(table_name, fix, primary_key, data['shop_id'])
        log.msg('SQL: %s' % sql, _level=log.INFO)
        return sql

    def __init__(self):
        self.connect = MySQLdb.connect(user=settings.MYSQL_DB_USER,
                                       passwd=settings.MYSQL_DB_PASSWORD,
                                       db=settings.MYSQL_DB_NAME,
                                       host=settings.MYSQL_DB_HOST,
                                       port=settings.MYSQL_DB_PORT,
                                       charset=settings.MYSQL_DB_CHARSET)
        self.cursor = self.connect.cursor()
        self.connect.commit()
        # self.connect.set_character_set('utf-8')
        self.base_spiders = settings.BASE_SPIDER
        self.detail_spider = settings.DETAIL_SPIDER
        pass

