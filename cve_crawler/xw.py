#coding:utf-8
# 玄武实验室secnews 爬取与解析
import sys,os,re
import requests
import time
from datetime import datetime, timedelta

def get_html(url):
    page = requests.get(url, verify=False)
    print url
    return page.content

def date_range(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date +timedelta(n)

def create_urls(start_date, end_date):
    urls = {}
    host = 'https://xuanwulab.github.io/cn/secnews/%s/%s/%s/index.html'
    for i in date_range(start_date, end_date):
        year, month, day = str(i.year), str(i.month), str(i.day)
        if i.month < 10:
            month = "0" + str(i.month)
        if i.day < 10:
            day = "0" + str(i.day)
        dt = "%s-%s-%s" % (year, month, day)
        urls[dt] = host % (year, month, day)
    return urls

def crawler_xw():
    '''
    设置玄武信息的开始时间和结束时间，即可开始爬虫
    '''
    start_date = datetime(2018,6,1)
    end_date = datetime(2018,6,5)

    urls = create_urls(start_date, end_date)
    root_path = 'E:/xuanwulab'
    if not os.path.isdir(root_path):
        os.mkdir(root_path)
    for date, url in urls.items():
        try:
            with open('%s/%s.html' % (root_path,date), 'w+') as f:
                f.write(get_html(url))
        except Exception, e:
            print date, e


# 存储新版本内容文件
xw_new_version_txt = 'E:/xw_new_version_txt.txt'
# 存储旧版本内容
xw_old_version_txt = 'E:/xw_old_version_txt.txt'

def get_path(root_dir):
    '''
    找出某个路径下所有文件
    :param root_dir: 根目录
    :return: 文件路径列表
    '''
    list_dirs = os.walk(root_dir)
    paths = []
    for root, dirs, files in list_dirs:
        for f in files:
            paths.append(os.path.join(root, f))
    return paths

def parse_xw_html(path):
    '''
    解析html类型，主要过程为：
    1. 从文件中读取txt
    2. 替换txt某些特殊字符
    3. 找出具体条目
    4. 根据排版选择解析函数
    :param path: html存储路径
    :return: 条目个数
    '''
    txt = open(path, 'r').readlines()
    txt = "".join(txt).replace('\n','').replace('\t','').replace('\r','').replace('<br/>','').replace(',','. ').replace('\xc2\xa0','')
    txt = re.sub('\s+', ' ', txt)
    single_txts = re.findall(r'<div class="singleweibotext"><p>(.*?)</p></div>', txt, re.M|re.I)
    date = re.search(r'(20.*?)\.html', path, re.I)
    if date is None:
        date = "NULL"
    else:
        date = date.group(1)
    flag = False
    for each in single_txts:
        if each.find(r'<span class="category"') != -1:
            flag = True
            break
    if flag:
        parse_new_version(single_txts, date)
    else:
        parse_old_version(single_txts, date)
    return len(single_txts)

def parse_new_version(single_txts, date):
    '''
    解析新排版html，2016年6月1日之后的排版，
    包括每个条目包括三个内容：category（类型）、des（描述）、links（链接）
    :param single_txts: 条目内容
    :param date: 日期
    :return: None
    '''
    st = []
    for each in single_txts:
        print each
        category = re.search(r'"category">(.*?)</span>', each, re.I)
        if category is not None:
            category = category.group(1)
        else:
            category = "NULL"
        des = re.search(r'</span>(.*?)<a href', each, re.I)
        if des is not None:
            des = des.group(1)
        else:
            des = "NULL"
        links = re.findall(r'<a href.*?>(.*?)</a>', each, re.I)
        if links is None or len(links) == 0:
            links = "NULL"
        else:
            links = "; ".join(links)
        st.append((date, category, des, links))

    with open(xw_new_version_txt, 'a+') as f:
        for ev in st:
            f.write(",".join(ev) + "\n")
        pass

def parse_old_version(single_txts, date):
    '''
    解析旧排版html，2016年6月1日之前的排版，
    包括每个条目包括四个内容：category（类型）、des（原始描述）、traslate（翻译）、links（链接）
    :param single_txts: 条目内容
    :param date: 日期
    :return: None
    '''
    st = []
    for each in single_txts:
        category = re.search(r'<i>(.*?)</i>', each, re.I)
        if category is not None:
            category = category.group(1)
        else:
            category = "NULL"
        des = re.search(r'</i>](.*?)<a href', each, re.I)
        if des is not None:
            des = des.group(1)
        else:
            des = "NULL"
        traslate = re.search(r'<p>(.*?)<a href', each, re.I)
        if traslate is not None:
            traslate = traslate.group(1)
        else:
            traslate = "NULL"
        links = re.findall(r'<a href.*?>(.*?)</a>', each, re.I)
        if links is None or len(links) == 0:
            links = "NULL"
        else:
            links = "; ".join(links)
        st.append((date, category, des, traslate, links))
    with open(xw_old_version_txt, 'a+') as f:
        for ev in st:
            f.write(",".join(ev) + "\n")
    pass

if __name__ == '__main__':
    crawler_xw()
