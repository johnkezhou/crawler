# coding:utf-8
from scrapy.selector import Selector

# body = open("../g101r7947_p1").read()
# select = Selector(text=body)
# page = select.xpath('//*[@id="top"]/div[6]/div[3]/div[1]/div[2]//*').extract()
# print page
# print len(page)
# shop_name = select.xpath('//*[@id="shop-all-list"]/ul/li[1]/div[2]/div[1]/a[1]/h4/text()').extract()[0]
# shop_name1 = select.xpath('//*[@id="shop-all-list"]/ul/li[2]/div[2]/div[1]/a[1]/h4/text()').extract()[0]
# shop_logo = select.xpath('//*[@id="shop-all-list"]/ul/li[1]/div[1]/a/img/@data-src').extract()[0]
# shop_logo1 = select.xpath('//*[@id="shop-all-list"]/ul/li[2]/div[1]/a/img/@data-src').extract()[0]
# shop_url = select.xpath('//*[@id="shop-all-list"]/ul/li[1]/div[2]/div[1]/a[1]/@href').extract()[0]
# shop_url1 = select.xpath().extract()[0]
# shop_level = select.xpath('//*[@id="shop-all-list"]/ul/li[1]/div[2]/div[2]/span/@title').extract()[0]
# shop_level1 = select.xpath().extract()[0]
# comment_number = select.xpath('//*[@id="shop-all-list"]/ul/li[1]/div[2]/div[2]/a[1]/b/text()').extract()[0]
# comment_number1 = select.xpath().extract()[0]
# avgcost = select.xpath('//*[@id="shop-all-list"]/ul/li[1]/div[2]/div[2]/a[2]/b/text()').extract()[0]
# avgcost1 = select.xpath().extract()[0]
# taste = select.xpath('//*[@id="shop-all-list"]/ul/li[1]/div[2]/span/span[1]/b/text()').extract()[0]
# taste1 = select.xpath().extract()[0]
# environment = select.xpath('//*[@id="shop-all-list"]/ul/li[1]/div[2]/span/span[2]/b/text()').extract()[0]
# environment1 = select.xpath().extract()[0]
# service = select.xpath('//*[@id="shop-all-list"]/ul/li[1]/div[2]/span/span[3]/b/text()').extract()[0]
# service1 = select.xpath().extract()[0]
# food_type = select.xpath('//*[@id="shop-all-list"]/ul/li[1]/div[2]/div[3]/a[1]/span/text()').extract()[0]
# food_type1 = select.xpath().extract()[0]
# location = select.xpath('//*[@id="shop-all-list"]/ul/li[1]/div[2]/div[3]/a[2]/span/text()').extract()[0]
# location1 = select.xpath().extract()[0]
# address = select.xpath('//*[@id="shop-all-list"]/ul/li[1]/div[2]/div[3]/span/text()').extract()[0]
# address1 = select.xpath().extract()[0]
#
# tuan = select.xpath('//*[@id="shop-all-list"]/ul/li[8]/div[2]/div[1]/div/a[1]').extract()
# tuan_url = select.xpath('//*[@id="shop-all-list"]/ul/li[8]/div[2]/div[1]/div/a[1]/@href').extract()[0]
# tuan_title = select.xpath('//*[@id="shop-all-list"]/ul/li[8]/div[2]/div[1]/div/a[1]/@title').extract()[0]
# tuan = select.xpath('//*[@id="shop-all-list"]/ul/li[8]/div[3]/div/a[2]/@href').extract()
# tuan = select.xpath('//*[@id="shop-all-list"]/ul/li[8]/div[3]/div/a[3]/@href').extract()
# wai = select.xpath('//*[@id="shop-all-list"]/ul/li[13]/div[2]/div[1]/div/a[2]/@title').extract()[0]
# cu = select.xpath('//*[@id="shop-all-list"]/ul/li[14]/div[2]/div[1]/div/a[2]/@title').extract()[0]
# branch = select.xpath('//*[@id="shop-all-list"]/ul/li[13]/div[2]/div[1]/a[2]/text()').extract()[0]
#
# print shop_name
# print shop_logo
# print shop_url
# print shop_level
# print comment_number
# print avgcost[1:]
# print tuan
# print tuan_url
# print tuan_title
# print wai
# print cu
# print branch
import random,os, time, re

data = open('../pipeline_shop').read().split("\n")
data = list(set(data))
with open('../pipeline_shop','w') as fw:
    fw.write("\n".join(data))

def append_urls(text, url):
    try:
        page = re.findall('data-ga-page', text, re.M)
        url_list = []
        if page == None or len(page) == 0:
            return
        page_list = range(2, len(page))
        random.shuffle(page_list)
        for pl in page_list:
            url_list.append(url + "p%s" % pl)
        if len(page) == 0:
            return
        with open('D:/idea-workspace/dianping_crawler/beyond_p1_tmp', 'a+') as fw:
            fw.write("\n".join(url_list) + "\n")
    except Exception as e:
        print e

def dirlist(path, allfile):
    filelist = os.listdir(path)
    for filename in filelist:
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            child_filelist = os.listdir(filepath)
            for cf in child_filelist:
                if cf.find("p1") != -1:
                    allfile.append(os.path.join(filepath, cf))
        else:
            allfile.append(filepath)
    return allfile

def filter_key(key):
    tmp = key.split('_')
    for i in range(1, len(tmp)):
        tmp[i] = tmp[i][0].upper() + tmp[i][1:]
    return ''.join(tmp)

def full_shop_url():
    shop_urls = open('../shop_urls').read().split("\n")
    uh = 'http://www.dianping.com'
    for i in range(len(shop_urls)):
        shop_urls[i] = uh + shop_urls[i]
    with open('../shop_urls', 'w') as fw:
        fw.write("\n".join(shop_urls))
    fw.close()

def filter_menu_url():
    menu_url = open('../menu_urls').read().split("\n")
    tmp = open('../shop.txt').read().split("\n")
    shop_id = []
    cm = []
    for ev in tmp:
        tp = ev.split(",")
        shop_id.append(tp[0])
        cm.append(int(tp[1]))

    murl = []
    for mv in menu_url:
        for i in range(len(shop_id)):
            if mv.find(shop_id[i]) != -1 and cm[i] >= 50:
                murl.append(mv)
                break

    with open('../menu_urls_50', 'w') as fw:
        fw.write("\n".join(murl))
    fw.close()
import settings
import MySQLdb
connect = MySQLdb.connect(user=settings.MYSQL_DB_USER,
                          passwd=settings.MYSQL_DB_PASSWORD,
                          db=settings.MYSQL_DB_NAME,
                          host=settings.MYSQL_DB_HOST,
                          port=settings.MYSQL_DB_PORT,
                          charset=settings.MYSQL_DB_CHARSET)
cursor = connect.cursor()
connect.commit()
def build_review_url():
    review_url_file = open("../review_urls",'a+')

fix_keys = ['shop_name', 'full_name', 'phone', 'shop_group_id', 'city_id', 'city_name', 'shop_glat', 'shop_glng', 'power', 'shop_power', 'shop_type', 'main_category_id','vote_total', 'district', 'public_transit', 'shop_info']
sql_file = open("../sql_file",'a+')
def full_data_sql(id, dt):
    sql = 'UPDATE shop SET '
    fix_dict = {}
    for key in fix_keys:
        fix_dict[key] = ''
    for key in fix_dict:
        fkey = filter_key(key)
        if fkey in dt and dt[fkey] != '':
            fix_dict[key] = dt[fkey]
    condi = []
    for key, value in fix_dict.items():
        if value != '':
            condi.append("%s='%s'" %(key, value))
    sql += "%s WHERE shop_id=%s;" % (",".join(condi), id)
    sql_file.write(sql + "\n")

def build_user_url():
    data = cursor.execute('SELECT user_id FROM user;')
    rows = cursor.fetchall()
    user_ids = []
    for row in rows:
        user_ids.append("http://www.dianping.com/member/%s"%row[0])
    with open('../user_urls','w') as fw:
        fw.write("\n".join(user_ids))

def full_data():
    data = cursor.execute('SELECT shop_id FROM shop WHERE power != "5";')
    rows = cursor.fetchall()
    shop_ids = []
    for row in rows:
        shop_ids.append(row[0])
    shop_configs = open('../pipeline_shopconfig').read().split("\n")
    for i in range(len(shop_configs)):
        shop_configs[i] = eval(shop_configs[i])
    for id in shop_ids:
        for config in shop_configs:
            if 'shopId' in config and str(config['shopId']) == id:
                full_data_sql(id, config)
                break


def build_review_url():
    data = cursor.execute('SELECT shop_id FROM shop WHERE power = "5" AND comment_number >= 50;')
    rows = cursor.fetchall()
    shop_ids = []
    for row in rows:
        shop_ids.append(row[0])
    review_urls = []
    url = '&cityId=3&categoryURLName=food&power=5&cityEnName=hangzhou&shopType=10'
    head = 'http://www.dianping.com/ajax/json/shopDynamic/allReview?shopId='
    for id in shop_ids:
        review_urls.append(head+id+url)
    with open('../review_urls','w') as fw:
        fw.write("\n".join(review_urls))
    fw.close()

def cout_items():
    data = eval(open('../review.json').read().replace('true','True').replace('false','False').replace('null','""'))
    reviewlist = data['reviewAllDOList']
    for key in reviewlist[0].keys():
        print transform_key(key)
    return data


def recursion_dict(dt, level):
    level += 1
    for key, value in dt.items():
        print "".join(["    "]*level+[transform_key(str(key)) + " = scrapy.Field()"])
        if isinstance(value, list):
            value = value[0]
        if isinstance(value, dict):
            recursion_dict(value,level)


def transform_key(key):
    tmp = []
    for i in range(len(key)):
        if key[i] >= 'A' and key[i] <= 'Z':
            tmp.append("_%s" % key[i].lower())
        else:
            tmp.append(key[i])
    return "".join(tmp)

if __name__ == '__main__':
    # recursion_dict(cout_items(),0)
    # cout_items()
    build_user_url()