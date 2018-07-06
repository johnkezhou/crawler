
# --*-- coding:UTF-8 --*--
import re
import time
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
class selectUserinfo(object):

    def __init__(self, html,yukelog):
        '''
        Constructor
        '''
        self.html = html
        self.getUserInfo()
        self.yukelog = yukelog
    def getpageNum(self,html):
        page = re.search('name="mp".*?value="(.*?)" /><input', html, re.S)
        if page is None:
            pageNum = 1
        else:
            pageNum = (int)(page.group(1))
        return pageNum
    def getUserInfo(self):
        userInfo = {}
        uhtml = self.searchtmp('<div class="u">(.*?)</div><div', self.html)
        tmp = re.findall('(<span class="ctt".*?</span>)', uhtml, re.S)
        userInfo['pn'] = self.getpageNum(self.html)
        print "tmp = %d" % len(tmp)
        if len(tmp) is 2:
            print tmp[0]
            print tmp[1]
#             print tmp
            userInfo['de'] = self.searchPattern('width:50px;">(.*?)</span>', tmp[1])
            userInfo['vi'] = "not find"                                             #verify_info
            userInfo['un'] = self.searchPattern('class="ctt">(.*?)&nbsp', tmp[0])         #username
            userInfo['sx'] = self.searchPattern('&nbsp;(.*?)/', tmp[0])       #sex
            userInfo['ad'] = self.searchPattern('/(.*?)&nbsp;    <span', tmp[0])        #address
            if re.search('<img =src(.*?)>', tmp[0], re.S) is None:
                userInfo['dr'] = self.searchPattern('alt="(.)"', tmp[0]) 
            else:
                userInfo['dr'] = "not find" 
        if len(tmp) is 3:
#             print tmp
            userInfo['de'] = self.searchPattern('width:50px;">(.*?)</span>', tmp[2])
            userInfo['vi'] = self.searchPattern('<span class="ctt">(.*?)</span>', tmp[1])                               #verify_info
            userInfo['un'] = self.searchPattern('class="ctt">(.*?)&nbsp', tmp[0])         #username
            userInfo['sx'] = self.searchPattern('&nbsp;(.*?)/', tmp[0])       #sex
            userInfo['ad'] = self.searchPattern('&nbsp;.*?/(.*?)&nbsp;    <span', tmp[0])        #address
            if re.search('<img =src(.*?)>', tmp[0], re.S) is None:
                userInfo['dr'] = self.searchPattern('alt="(.)"', tmp[0])                     #is_daren
            else:
                userInfo['dr'] = "not find" 
        userInfo['wn'] = self.searchPattern('class="tc">(.*?)</span>', uhtml)#wei_num
        userInfo['an'] = self.searchPattern('/follow">(.*?)</a>', uhtml)   #attention_num
        userInfo['fn'] = self.searchPattern('/fans">(.*?)</a>', uhtml)     #fans_num
        userInfo['wn'] = self.getNum(userInfo['wn'])
        userInfo['an'] = self.getNum(userInfo['an'])
        userInfo['fn'] = self.getNum(userInfo['fn'])
        self.userInfo = userInfo
        return userInfo
    def getNum(self,tmp):
        if tmp is None:
            return tmp
        res = re.search(r'(\w*[0-9]+)\w*', tmp)
        if res is not None:
            return res.group(1)
        else:
            return tmp
    def searchPattern(self,pattern, string):
        searchResult = re.search(pattern, string, re.S)
        if searchResult is None:
            searchResult = "not find"
        else:
            searchResult = searchResult.group(1)
            searchResult = re.sub(r'<a href=".*?">', ' ', searchResult, re.S)
            searchResult = re.sub(r'</a>','',searchResult,re.S)
            searchResult = re.sub(r'&nbsp;', ' ', searchResult, re.S)
            searchResult = re.sub(r'<img src=".*?"/>', ' ', searchResult, re.S)
        return searchResult
    def searchtmp(self,pattern, string):
        searchResult = re.search(pattern, string, re.S)
        if searchResult is None:
            searchResult = "not find"
        else:
            searchResult = searchResult.group(1)
        return searchResult
     
      
class selectFans(object):
    
    def __init__(self, htmllist,yukelog):
        '''
        Constructor
        '''
        self.htmllist = htmllist
        self.getAllFansInfo
        self.yukelog = yukelog
    def getFansList(self,html):
        fanslist = re.findall(r'<table>(.*?)</table>', html, re.S)
        return fanslist
    
    def getFansInfo(self,fanslist):
        fansinfo = {}
        fansinfo['fid'] = self.searchPattern('uid=(.*?)&', fanslist)
        fansinfo['fun'] = self.searchPattern('valign="top">.*?">(.*?)</a>', fanslist)
        fansinfo['ffn'] = self.searchPattern('<br/>(.*?)<br/>', fanslist)
        tmp = re.search(r'(\w*[0-9]+)\w*', fansinfo['ffn'])
        if tmp is not None:
            fansinfo['ffn'] = tmp.group(1)
        return fansinfo
        
    def getAllFansInfo(self):
        fansinfo = []
        index = 0
        page = 0
        for html in self.htmllist:
            fanslist = self.getFansList(html)
            for each in fanslist:
                data = self.getFansInfo(each)
                fansinfo.append(data)
                index = index +1
                self.yukelog.logging("第" + str(index) + "个 粉丝信息 提取成功","info")
            page = page + 1
            self.yukelog.logging("第" + str(page) + "页 粉丝列表 爬取成功","info")    
        return fansinfo
    
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

class selectAttenion(object):
        
    def __init__(self, htmllist,yukelog):
        '''
        Constructor
        '''
        self.htmllist = htmllist
        self.yukelog = yukelog
    def getAttentionList(self,html):
        Attentionlist = re.findall(r'<table>(.*?)</table>', html, re.S)
        return Attentionlist
    def getAttentionInfo(self,Attentionlist):
        Attentioninfo = {}
        Attentioninfo['aid'] = self.searchPattern('uid=(.*?)&', Attentionlist)
        Attentioninfo['aun'] = self.searchPattern('valign="top">.*?">(.*?)</a>', Attentionlist)
        Attentioninfo['afn'] = self.searchPattern('<br/>(.*?)<br/>', Attentionlist)
        tmp = re.search(r'(\w*[0-9]+)\w*', Attentioninfo['afn'])
        if tmp is not None:
            Attentioninfo['afn'] = tmp.group(1)
        return Attentioninfo

    def getAllAttentionsInfo(self):
        Attentionsinfo = []
        index = 0
        page = 0
        for html in self.htmllist:
            Attentionslist = self.getAttentionList(html)
            for each in Attentionslist:
                data = self.getAttentionInfo(each)
                Attentionsinfo.append(data)
                index = index +1
                self.yukelog.logging("第" + str(index) + "个 关注人信息 提取成功","info")
            page = page + 1
            self.yukelog.logging("第" + str(page) + "页 关注人列表 爬取成功","info")    
        return Attentionsinfo
        
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
    
if __name__ == '__main__':
    
    print u"是的吧"
        
        
        
        
        
        
        
        
        