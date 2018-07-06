
# --*-- coding:UTF-8 --*--
from downloader import download
from selector import *
from CrawlerWeibo import crawlerweibo
from Log import yklog
import os
import datetime
import sys
reload(sys)

sys.setdefaultencoding( "utf-8" )
#爬虫代码
class crawler(object):
    
    def __init__(self,uid):
        self.uid = uid
        self.geturllist()
        self.path = "D:/weibouser/"
        self.yukelog = yklog(self.uid)
    #构造url池
    def geturllist(self):
        self.urllist = {}
        url = 'http://weibo.cn/%s'% self.uid
        self.urllist['profile'] = url + '/profile?page=1'
        self.urllist['attention'] = url + '/follow?page=1'
        self.urllist['fans'] = url + '/fans?page=1'
        self.urllist['atme'] = 'http://weibo.cn/at/weibo?uid=%s'%self.uid
    #存储关注列表信息
    def saveattInfo(self,info):
        flag = os.path.exists(self.path + self.uid)
        if flag:
            print "dir exist"
        else:
            os.mkdir(self.path + self.uid)
        path = self.path + self.uid + '/' + "attention.txt";
        finfo = open(path,'w')
        index = 1
        for each in info:
            res = "\"" + self.uid + "-" + str(index) + "\" \"" + self.uid + "\" \"" + each['aid'] + "\" \"" + each['aun'] + "\" \"" + each['afn'] + "\"\n"
            finfo.write(res)
            index = index + 1
        finfo.close()
        return
    #存储粉丝信息
    def savefansInfo(self,info):
        flag = os.path.exists(self.path + self.uid)
        if flag:
            print "dir exist"
        else:
            os.mkdir(self.path + self.uid)
        path = self.path + self.uid + '/' + "fans.txt"
        finfo = open(path,'w')
        index = 1
        for each in info:
            res = "\"" + self.uid + "-" + str(index) + "\" \"" + self.uid + "\" \"" + each['fid'] + "\" \"" + each['fun'] + "\" \"" + each['ffn'] + "\"\n"
            finfo.write(res)
            index = index + 1
        finfo.close()
        return
    #存储微博信息
    def saveWeiboInfo(self,info):
        time.sleep(2)
        flag = os.path.exists(self.path + self.uid)
        if flag:
            print "dir exist"
        else:
            os.mkdir(self.path + self.uid)
        path = self.path + self.uid + '/' + "weiboinfo.txt"
        finfo = open(path,'a')
        for each in info:
            for key in each:
                if each[key] is None:
                    each[key] = ' '
            res = "\"" + each['id'] + "\" \"" + each['mc'] + "\" \"" + each['uid'] + "\" \"" + each['mt'] + "\" \"" + each['ot'] + "\" \"" + each['oui'] + "\" \"" + each['oun'] + "\" \"" + each['ozc'] + "\" \"" + each['occ'] + "\" \"" + each['orc'] + "\" \"" + each['zc'] + "\" \"" + each['cc'] + "\" \"" + each['rc'] +"\" \"" + each['it'] +"\" \"" + each['is'] +"\"\n"
            print res
            finfo.write(res)
        finfo.close()
        return
    #存储用户信息
    def saveuserInfo(self,info):
        flag = os.path.exists(self.path + self.uid)
        if flag:
            print "dir exist"
        else:
            os.mkdir(self.path + self.uid)
        path = self.path + self.uid + "/userinfo.txt"
        finfo = open(path,'w')
        res = ""
        #sx ad vi de an dr un wn pn fn cwn uid
        for key in info:
            if info[key] is None:
                info[key] = ' '
        res = "\"" + info['uid'] + "\" \"" + info['un'] + "\" \"" + info['sx'] + "\" \"" + info['ad'] + "\" \"" + info['vi'] + "\" \"" + info['de'] + "\" \"" + str(info['wn']) + "\" \"" + str(info['an']) + "\" \"" + str(info['fn']) + "\" \"" + info['dr'] + "\" \"" + info['cwn'] + "\" \"" + str(info['pn']) +"\"\n"
        print res
        finfo.write(res)
        finfo.close()
    def saveflagweibo(self):
        if len(self.wb) < 1:
            return
        print 
        info = self.wb[0]

        flag = os.path.exists(self.path + self.uid)
        if flag:
            print "dir exist"
        else:
            os.mkdir(self.path + self.uid)
        path = self.path + self.uid + '/flagweibo.txt'
        finfo = open(path,'w')
        res = str(info['it']) + '\n' + str(info['mc'])
        finfo.write(res)
        finfo.close()
    
    def iscrawed(self):
        uidlist = os.listdir(self.path)    
        if self.uid in uidlist:
            txtlist = os.listdir(self.path +self.uid + '/');
            if 'flagweibo.txt' in txtlist:
                #代表这个号只更新微博
                return 1;
            else:
                #代表这个号只有微博正文部分没有爬
                return 0
        else:
            #代表这个号没有爬过
            return 2
        
    
    def getAttention(self,path):
        if not os.path.exists(path):
            return None
        else:
            file = open(path)
            line = file.readlines()
            uidlist = []
            for each in line:
                a = each.split(' ')
                b = re.search(r'\"(.*)\"', a[2])
                if b is not None:
                    uidlist.append(b.group(1))
            return uidlist
        
    def crawling(self,fans,atten,weibo,user):
        timestart = datetime.datetime.now()
        
        print self.uid + "==============================================", self.iscrawed()
        down = download(self.urllist)
        #只更新当前账号微博
        tj = str(1)
        print fans, ' ', atten, ' ', weibo, ' ', user
        if self.iscrawed() is 1:
            msg = self.uid + "    更新当前账号微博信息"
            self.yukelog.logging(msg, "info")
            path = self.path + self.uid + '/attention.txt'
            self.att = self.getAttention(path)
            flag = self.readFlag()
            if weibo is tj:
                self.crawlerWeibo(flag)
#             return
        #该账号未爬取过
        if self.iscrawed() is 2:
            msg = self.uid + "    新账号微博信息爬取"
            self.yukelog.logging(msg, "info")
            flag = None
            #爬取粉丝部分
            if fans is tj :
                self.crawlerFans(down)
                
            #爬取关注列表部分
            if atten is tj :
                self.crawlerAtten(down)
            if user is tj :
                self.crawlerUser(down)
            if weibo is tj :
                self.crawlerWeibo(flag)
            
#             return
        #更新当前微博信息
        if self.iscrawed() is 0:
            msg = self.uid + "    更新当前账号微博信息，但不更新用户信息"
            self.yukelog.logging(msg, "info")
            flag = None
            path = self.path + self.uid + '/attention.txt'
            self.att = self.getAttention(path)
#             if user is tj:
#                 self.crawlerUser(down)
            if weibo is tj:
                self.crawlerWeibo(flag)
        msg = self.uid + "    当次爬取完成"
        self.yukelog.logging(msg, "info")
        timeend = datetime.datetime.now()
        msg = "当次爬虫用时为（包括间隔访问时间） ：" + str(timeend - timestart)
        self.yukelog.logging(msg, "info")
        self.yukelog.close()
    def crawlerUser(self,down):
        ui = selectUserinfo(down.userinfoDownload(),self.yukelog).getUserInfo()
        ui['cwn'] = None
        ui['uid'] = self.uid
        self.saveuserInfo(ui)
        self.yukelog.logging("用户信息爬取完毕","info")
    def crawlerFans(self,down):
        fans = selectFans(down.fansDownload(),self.yukelog).getAllFansInfo()
        self.fans = fans
        self.savefansInfo(fans)
        self.yukelog.logging("粉丝信息爬取完毕","info")
        self.yukelog.logging("获取到的粉丝人数为 ："+str(len(fans)),"info")
    def crawlerAtten(self,down):
        att = selectAttenion(down.attentionDownload(),self.yukelog).getAllAttentionsInfo()
        self.att = []
        for each in att:
            self.att.append(each['aid'])
        self.saveattInfo(att)
        self.yukelog.logging("关注信息爬取完毕","info")
        self.yukelog.logging("获取到的关注人数为 ："+str(len(att)),"info")
    def readAtten(self):
        path = self.path + self.uid + '/attention.txt'
        self.att = self.getAttention(path)
        self.yukelog.logging("关注列表读取成功","info")
    def readFlag(self):
        f = open(self.path + self.uid + '/flagweibo.txt','r')
        time = f.readlines()
        f.close()
        flag = {}
        flag['it'] = time[0]
        flag['mc'] = time[1]
        self.yukelog.logging("flag信息成功获取","info")
        return flag
    
    def crawlerWeibo(self,flag):
        print "crawlerWeibo"
        wb = crawlerweibo(self.urllist['profile'],self.uid,flag,self.yukelog).weiboDownload()
        self.wb = wb
        print "lenweb: ",len(wb)
        self.saveflagweibo() 
        self.saveWeiboInfo(wb)
        self.yukelog.logging("微博文本爬取完毕","info")
        self.yukelog.logging("当次获取微博文本数 ："+str(len(wb)),"info")
    
    
if __name__ == '__main__':
    
    uid = "1312893987"
    fans = "1"
    atten = "1"
    weibo = "1"
    user = "1"
    print uid, ' ', fans, ' ', atten, ' ', weibo, ' ', user
    try:
        craw = crawler(uid)
        craw.crawling(fans,atten,weibo,user)
    except Exception,e:
        print e
    else:
        print True
    
    child = "1"
    grandchild = "0"
    uid_num = 1
    tj = str(1)
    if child is tj:
        child = craw.att
        tree = []
        for each in child:
            print each
            ce = crawler(each)
            ce.crawling(fans,atten,weibo,user)
            uid_num = uid_num + 1;
            if uid_num % 10 == 0:
                time.sleep(900)
            tree.append(ce.att)
    if grandchild is tj:
        for node in tree:
            for every in node:
                tmp = crawler(every)
                tmp.crawling()
                uid_num = uid_num + 1;
                if uid_num % 10 == 0:
                    time.sleep(900)
 