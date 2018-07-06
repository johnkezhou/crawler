
# --*-- coding:UTF-8 --*--
from cookie import cookies
import requests
import time
import re
import random

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
#
class crawlerweibo(object):
    '''
    classdocs
    '''
    def __init__(self, url,uid,flag,yukelog):
        '''
        Constructor
        '''
        self.cookie = cookies()
        self.url = url
        self.uid = uid
        self.flag = flag
        self.index = 0
        self.yukelog = yukelog
    def gethtmltext(self,url):
        print url
        self.yukelog.logging(url, "info")
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
            if pageNum > 100:
                pageNum = 100
        print pageNum
        self.yukelog.logging("当前账号爬取微博页数为：" + str(pageNum),"info")
        return pageNum

    def weiboDownload(self):
        weibohtml = [];
        weibodetail = []
        url = self.url
        html = self.gethtmltext(url)
        self.userinfo = html
        allpage = self.getpageNum(html)
        weibohtml.append(html)
        weibolists = self.getweiboList(html)
        index = 0
        if self.flag is None:
            for each in weibolists:
                data = self.getweiboInfo(each)
                data['id'] = self.uid + '**' + data['it']
                weibodetail.append(data)
                index = index + 1
                self.yukelog.logging("第" + str(index) + "条 微博 提取成功","info")
            self.yukelog.logging("第" + str(1) + "页 微博 爬取成功","info")
            for i in range(2,allpage+1):
                newurl = re.sub(r'page=\d+', 'page=%s'%i, url, re.S)
                html = self.gethtmltext(newurl)
                weibolists = self.getweiboList(html)
                for each in weibolists:
                    data = self.getweiboInfo(each)
                    data['id'] = self.uid + '**' + data['it']
                    weibodetail.append(data)
                    index = index + 1
                    self.yukelog.logging("第" + str(index) + "条 微博 提取成功","info")
                weibohtml.append(html)
                self.yukelog.logging("第" + str(i) + "页 微博 爬取成功","info")
            self.weibohtml = weibohtml
            return weibodetail
        else:
            for each in weibolists:
                data = self.getweiboInfo(each)
                data['id'] = self.uid + '**' + data['it']
                if not self.isTimeover(data['it'],self.flag['it']):
                    print len(weibodetail)
                    return weibodetail
                weibodetail.append(data)
                index = index + 1
                self.yukelog.logging("第" + str(index) + "条 微博 提取成功","info")
            self.yukelog.logging("第" + str(1) + "页 微博 爬取成功","info")
            for i in range(2,allpage+1):
                newurl = re.sub(r'page=\d+', 'page=%s'%i, url, re.S)
                html = self.gethtmltext(newurl)
                weibolists = self.getweiboList(html)
                for each in weibolists:
                    data = self.getweiboInfo(each)
                    data['id'] = self.uid + '**' + data['it']
                    if not self.isTimeover(data['it'],self.flag['it']):
                        return weibodetail
                    weibodetail.append(data)
                    index = index + 1
                    self.yukelog.logging("第" + str(index) + "条 微博 提取成功","info")
                weibohtml.append(html)
                self.yukelog.logging("第" + str(i) + "页 微博 爬取成功","info")
            self.weibohtml = weibohtml
            
            return weibodetail

    def getweiboList(self,html):
        weiboList = re.findall(r'(<div class="c" id=".*?</div>)<div class="s"', html, re.S)
        return weiboList
        
    def getweiboInfo(self,weiboList):
        weiboInfo = {}
        weiboInfo['uid'] = self.uid
        wbinfo = re.findall(r'<div>(.*?)</div>', weiboList, re.S)
        if len(wbinfo) == 2:
            originalwb = wbinfo[0]
            repostwb = wbinfo[1]
            test = re.search(r'class="cmt"(.*?)</span>', originalwb, re.S)
            
            if test is None:
                weiboInfo['mt'] = 'original'
                weiboInfo['oui'] = None
                weiboInfo['ozc'] = None
                weiboInfo['orc'] = None
                weiboInfo['ot'] = None
                weiboInfo['occ'] = None
                weiboInfo['oun'] = None
                tmp = re.search(r'<span class="ctt">(.*?)<a href=.*?">(.*?)</a>', originalwb, re.S)
                if tmp is None:
                    weiboInfo['mc'] = "not find"
                else:
                    try:
                        weiboInfo['mc'] = tmp.group(1) + tmp.group(2)
                    except IndexError:
                        weiboInfo['mc'] = "not find"
            else:
                weiboInfo['mt'] = 'transmit'
                weiboInfo['oui'] = self.searchPattern('weibo.cn/u/(.*?)">', originalwb)
                weiboInfo['oun'] = self.searchPattern('weibo.cn/.*?">(.*?)</a>', originalwb)
                weiboInfo['ot'] = self.searchPattern('<span class="ctt">(.*?)</span>', originalwb)
                tmp = re.findall(r';<span class="cmt">(.*?)</span>', originalwb, re.S)
                if tmp is None:
                    weiboInfo['ozc'] = "not find"
                    weiboInfo['orc'] = "not find"
                else:
                    if len(tmp) < 2:
                        try:
                            weiboInfo['ozc'] = tmp[0]
                            weiboInfo['orc'] = "not find"
                        except IndexError:
                            weiboInfo['ozc'] = "not find"
                            weiboInfo['orc'] = "not find"
                    else:
                        weiboInfo['ozc'] = tmp[0]
                        weiboInfo['orc'] = tmp[1]
                weiboInfo['occ'] = self.searchPattern('class="cc">(.*?)</a>', originalwb)
                weiboInfo['mc'] = self.searchPattern('<span class="cmt">.*?</span>(.*?)&nbsp', repostwb)
            weiboInfo['zc'] = self.searchPattern('weibo.cn/attitude/.*?">(.*?)</a>', repostwb)
            weiboInfo['rc'] = self.searchPattern('weibo.cn/repost/.*?">(.*?)</a>', repostwb)
            weiboInfo['cc'] = self.searchPattern('class="cc">(.*?)</a>', repostwb)
            tmp = self.searchtmp('(<span class="ct">.*?</span>)', repostwb)
            weiboInfo['it'] = self.searchPattern('"ct">(.*?)&nbsp;', tmp)
            weiboInfo['is'] = self.searchPattern('&nbsp;(.*?)</span>', tmp)
        else:
            if len(wbinfo) == 1:
                repostwb = wbinfo[0]
                weiboInfo['mt'] = "original"
                weiboInfo['oui'] = None
                weiboInfo['ozc'] = None
                weiboInfo['orc'] = None
                weiboInfo['ot'] = None
                weiboInfo['occ'] = None
                weiboInfo['oun'] = None
                weiboInfo['mc'] = self.searchPattern('<span class="ctt">(.*?)</span>&', repostwb)
                arc = re.findall(r'<a href=.*?">(.*?)</a>&', repostwb, re.S)
                if arc is None:
                    weiboInfo['zc'] = "none"
                    weiboInfo['rc'] = "none"
                    weiboInfo['cc'] = "none"
                else:
                    weiboInfo['zc'] = self.searchPattern('weibo.cn/attitude/.*?">(.*?)</a>', repostwb)
                    weiboInfo['rc'] = self.searchPattern('weibo.cn/repost/.*?">(.*?)</a>', repostwb)
                    weiboInfo['cc'] = self.searchPattern('class="cc">(.*?)</a>', repostwb)
                tmp = self.searchtmp('(<span class="ct">.*?</span>)', repostwb)
                weiboInfo['it'] = self.searchPattern('"ct">(.*?)&nbsp;', tmp)
                weiboInfo['is'] = self.searchPattern('&nbsp;(.*?)</span>', tmp)
            else:
                if len(wbinfo) == 3:
                    originalwb = wbinfo[0]
                    archtml = wbinfo[1]
                    repostwb = wbinfo[2]
                    weiboInfo['mt'] = 'transmit'
                    weiboInfo['oui'] = self.searchPattern('weibo.cn/u/(.*?)">', originalwb)
                    weiboInfo['oun'] = self.searchPattern('weibo.cn/.*?">(.*?)</a>', originalwb)
                    weiboInfo['ot'] = self.searchPattern('<span class="ctt">(.*?)</span>', originalwb)
                    tmp = re.findall(r';<span class="cmt">(.*?)</span>', archtml, re.S)
                    if tmp is None:
                        weiboInfo['ozc'] = "not find"
                        weiboInfo['orc'] = "not find"
                    else:
                        if len(tmp) < 2:
                            try:
                                weiboInfo['ozc'] = tmp[0]
                                weiboInfo['orc'] = "not find"
                            except IndexError:
                                weiboInfo['ozc'] = "not find"
                                weiboInfo['orc'] = "not find"
                        else:
                            weiboInfo['ozc'] = tmp[0]
                            weiboInfo['orc'] = tmp[1]
                    weiboInfo['occ'] = self.searchPattern('class="cc">(.*?)</a>', archtml)
                    weiboInfo['mc'] = self.searchPattern('<span class="cmt">.*?</span>(.*?)&nbsp', repostwb)
#                     arc = re.findall(r'<a href=.*?">(.*?)</a>&', repostwb, re.S)
                    weiboInfo['zc'] = self.searchPattern('weibo.cn/attitude/.*?">(.*?)</a>', repostwb)
                    weiboInfo['rc'] = self.searchPattern('weibo.cn/repost/.*?">(.*?)</a>', repostwb)
                    weiboInfo['cc'] = self.searchPattern('class="cc">(.*?)</a>', repostwb)
                    tmp = self.searchtmp('(<span class="ct">.*?</span>)', repostwb)
                    weiboInfo['it'] = self.searchPattern('"ct">(.*?)&nbsp;', tmp)
                    weiboInfo['is'] = self.searchPattern('&nbsp;(.*?)</span>', tmp)
        weiboInfo['it'] = self.setTime(weiboInfo['it'])
        weiboInfo['zc'] = self.getNum(weiboInfo['zc'])
        weiboInfo['rc'] = self.getNum(weiboInfo['rc'])
        weiboInfo['cc'] = self.getNum(weiboInfo['cc'])
        weiboInfo['ozc'] = self.getNum(weiboInfo['ozc'])
        weiboInfo['orc'] = self.getNum(weiboInfo['orc'])
        weiboInfo['occ'] = self.getNum(weiboInfo['occ'])
        
        return weiboInfo
    def getNum(self,tmp):
        if tmp is None:
            return tmp
        res = re.search(r'(\w*[0-9]+)\w*', tmp)
        if res is not None:
            return res.group(1)
        else:
            return tmp
    def isTimeover(self,a,b):
                
        time = re.search(r'(.*?):(.*?):(.*?) (.*?):(.*?):(.*)', a)
        year = time.group(1)
        month = time.group(2)
        day = time.group(3)
        hour = time.group(4)
        min = time.group(5)
        second = time.group(6)
#         print year, month, day, ":", hour, min, second
        
        time1 = re.search(r'(.*?):(.*?):(.*?) (.*?):(.*?):(.*)', b)
        year1 = time.group(1)
        month1 = time.group(2)
        day1 = time.group(3)
        hour1 = time.group(4)
        min1 = time.group(5)
        second1 = time.group(6)
#         print year, month, day, ":", hour, min, second
        if year > year1:
            return True
        if month > month:
            return True
        if day > day1 :
            return True
        if hour > hour1:
            return True
        if min > min1:
            return True
    
    def setTime(self,isstime):
        isstime = isstime.decode('utf-8')
        year = (int)(time.strftime("%Y",time.localtime()))
        timenow = None
        if re.search(u"月", isstime) is not None:
            tmp = re.search(u'(.*?)月(.*?)日 (.*)', isstime)
            month = tmp.group(1)
            day = tmp.group(2)
            mini = tmp.group(3)
            timenow = str(year) + ':' + str(month) + ':' + str(day) + ' ' + str(mini) + ':00'
#             print timenow
            return timenow
        if re.search(u'今天', isstime) is not None:
            min = re.search(u'今天 (.*?)', isstime).group(1)
            month = (int)(time.strftime("%m",time.localtime()))
            day = (int)(time.strftime("%d",time.localtime()))
            timenow = str(year) + ":" + str(month) + ":" + str(day) + str(min) + ':00'
#             print timenow
            return timenow
        if re.search(u'分钟', isstime) is not None:
            month = (int)(time.strftime("%m",time.localtime()))
            day = (int)(time.strftime("%d",time.localtime()))
            t = (int)(re.search(u'(.*?)分', isstime).group(1))
            hour = (int)(time.strftime("%H",time.localtime()))
            min  = (int)(time.strftime("%M",time.localtime()))
            sec  = time.strftime("%S",time.localtime())
            min = min - t
            if min < 0:
                hour = hour - 1
                min = min + 60
                if hour < 0:
                    day = day - 1
                    hour = hour + 24
            timenow = str(year) + ":" + str(month) + ":" + str(day) + " " + str(hour) + ":" + str(min) + ":" + str(sec)
#             print timenow
            return timenow
        if timenow is None:
            isstime = re.sub('-', ':', isstime)
            return isstime
    
    def searchPattern(self,pattern, string):
        searchResult = re.search(pattern, string, re.S)
        if searchResult is None:
            searchResult = "not find"
        else:
            searchResult = searchResult.group(1)
            searchResult = re.sub(r'<a href=".*?">', ' ', searchResult, re.S)
            searchResult = re.sub(r'</a>','',searchResult,re.S)
            searchResult = re.sub(r'&nbsp;', ' ', searchResult, re.S)
        return searchResult
    def searchtmp(self,pattern, string):
        searchResult = re.search(pattern, string, re.S)
        if searchResult is None:
            searchResult = "not find"
        else:
            searchResult = searchResult.group(1)
        return searchResult
        
    


    
    
        