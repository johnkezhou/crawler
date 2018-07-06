
# --*-- coding:UTF-8 --*--
from cookie import cookies
import requests
import time
import re
import random
class download(object):
    '''
    classdocs
    '''
    def __init__(self, urllist):
        '''
        Constructor
        '''
        self.cookie = cookies()
        self.urllist = urllist
        self.index = 0
    def gethtmltext(self,url):
        print url
        ck = self.cookie.info
        time.sleep(random.uniform(2.5,3.5))
        begin = self.index
        for i in range(begin,3):
            each = ck[i]
            html = requests.get(url, cookies=each['cookie'], headers=each['header']).text
            flag = re.search(r'(<?xml version="1.0" encoding=.*?">)',html,re.S)
            if flag is not None:
                print html
                return html
            else:
                self.yukelog.logging("出现被封号现象，请注意","warnning")
                print "出现被封号现象，请注意"
                time.sleep(300)
                if self.index == 2:
                    self.index = 0
                else:
                    self.index = self.index + 1
        tmp = ck[1]
        
        html = requests.get(url, cookies=tmp['cookie'], headers=tmp['header']).text
        print "404"
        print html
        return html
    
    def getpageNum(self,html):
        page = re.search('name="mp".*?value="(.*?)" /><input', html, re.S)
        if page is None:
            pageNum = 1
        else:
            pageNum = (int)(page.group(1))
        return pageNum
    def userinfoDownload(self):
        url = self.urllist['profile']
        return self.gethtmltext(url)
    def weiboDownload(self):
        weibohtml = [];
        url = self.urllist['profile']
        
        html = self.gethtmltext(url)
        self.userinfo = html
        allpage = self.getpageNum(html)
        weibohtml.append(html)
        for i in range(2,allpage+1):
            newurl = re.sub(r'page=\d+', 'page=%s'%i, url, re.S)
            html = self.gethtmltext(newurl)
            weibohtml.append(html)
        return weibohtml
    
    def fansDownload(self):
        fanshtml = [];
        url = self.urllist['fans']
        html = self.gethtmltext(url)
        allpage = self.getpageNum(html)
        fanshtml.append(html)
        for i in range(2,allpage+1):
            newurl = re.sub(r'page=\d+', 'page=%s'%i, url, re.S)
            html = self.gethtmltext(newurl)
            fanshtml.append(html)
        return fanshtml
        
    def attentionDownload(self):
        attentionhtml = [];
        url = self.urllist['attention']
        html = self.gethtmltext(url)
        allpage = self.getpageNum(html)
        attentionhtml.append(html)
        for i in range(2,allpage+1):
            newurl  = re.sub(r'page=\d+', 'page=%s'%i, url, re.S)
            html = self.gethtmltext(newurl)
            attentionhtml.append(html)
        return attentionhtml
    
if __name__ == '__main__':
    
    
    url = "http://weibo.cn/u/1312893987?filter=1&page=2"
    downl = download(url)
    
    
        