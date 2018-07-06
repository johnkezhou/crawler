
# -*- coding: utf-8 -*-

import requests
import re
import time
import chardet

COOKIES = {'Cookie':'SCF=Akm4AHVUFYcecQ77sJlaUi2RLyQeIugYlBuGe7BzboLvFPF3eybdFoh85082jdLnCTRtSpotzqFyH8KgBaR0S5w.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhS4lH8KDekgFMkvO6Sf22i5JpX5KMhUgL.FozNeh.RSK-01hM2dJLoI742qg4.9gpDdc4kMGHRIBtt; _T_WM=64517b8935f29e9c888d8b419a9e2cce; H5_INDEX=3; H5_INDEX_TITLE=Dandelion_puxi; M_WEIBOCN_PARAMS=featurecode%3D20000320%26luicode%3D10000011%26lfid%3D102803_ctg1_8999_-_ctg1_8999_home%26fid%3D102803_ctg1_8999_-_ctg1_8999_home%26uicode%3D10000011; SUB=_2A250D57qDeThGeRJ61sZ9SvPwzuIHXVX8yKirDV6PUJbkdBeLU3FkW045-nbFDQTs2pGcoVVU3eTvBSxVQ..; SUHB=04W_frWVc5eg-d; SSOLoginState=1493954234'}
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

p = 0

def get_init_url(account):
    url_head = 'https://weibo.cn/%s'
    return url_head % account

def get_html(url):
    print url
    rq = requests.get(url=url, cookies=COOKIES, headers=HEADERS)
    html = rq.text
    # time.sleep(3)
    return html

def getpageNum(html):
    page = re.search('name="mp".*?value="(.*?)" /><input', html, re.S)
    try:
        if page is None:
            pageNum = 1
        else:
            pageNum = (int)(page.group(1))
    except Exception as e:
        return 1
    return pageNum

def get_weibo_body(html):
    try:
        pattern = '(<div class="c".*?<div class="s"></div>)'
        body = re.findall(pattern,html, re.S)
        return body
    except Exception as e:
        return []

def get_href_zutu(html):
    '''
    获取组图href
    :param html: 
    :return: 
    '''
    try:
        href = re.search(u'<a href="(.*?)">组图', html, re.S)
        if href is not None:
            return href.group(1)
        else:
            return None
    except Exception as e:
        return None

def get_href_yuantu(html):
    '''
    获取原图href
    :param html: 
    :return: 
    '''
    try:
        hrefs = re.findall(u'<span class="tc">.*?<a href="(.*?)">原图', html, re.S)
        if hrefs is not None:
            res = []
            for href in hrefs:
                href = "https://weibo.cn" + href
                href = href.replace(';','&')
                res.append(href)
            return res
        return hrefs
    except Exception as e:
        return []

def get_picture_url(href):
    '''
    获取原图url地址
    :param html: 
    :return: 
    '''
    print href
    rq = requests.get(url=href, cookies=COOKIES, headers=HEADERS)
    time.sleep(3)
    url = rq.url
    if url.endswith('.jpg') or url.endswith('.gif'):
        return rq.url
    html = rq.text
    pattern = 'src=".*?" width'
    try:
        url = re.search(pattern, html, re.S)
        if url is None:
            url = re.search(u'<a href="(https://wx.*?)">确定', html, re.S)
            if url is not None:
                return url.group(1)
            else:
                return "url-error"
        return url.group(1)
    except Exception as e:
        return "url-error"


def get_time_state(html):
    pattern = '<span class="ct">(.*?)&nbsp;(.*?)</span>'

def spider(account):
    init_url = get_init_url(account)
    weibo_html = get_html(init_url)
    weibo_body = get_weibo_body(weibo_html)
    for body in weibo_body:
        href = get_href_zutu(body)
        if href is None:
            pic = get_picture_url(ht)
            print pic
        else:
            zutu_html = get_html(href)
            yuantu_hrefs = get_href_yuantu(zutu_html)
            for ht in yuantu_hrefs:
                pic = get_picture_url(ht)
                print pic




if __name__ == '__main__':
    account = 'zhanghuiwen913'
    spider(account)

    href = 'https://weibo.cn/mblog/oripic?id=EBzL92Xsv&amp&u=005zXJpsly1fe07umxy67j31f01w04qu&amp&rl=1'
    print get_picture_url(href)