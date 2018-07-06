# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request

class WeiboCrawlSpider(scrapy.Spider):
    name = "weibo_crawl"
    allowed_domains = ["weibo.cn"]
    start_urls = ['https://weibo.cn/zhanghuiwen913']
    weibo_account = ''
    COOKIE = {'Cookie':'SCF=Akm4AHVUFYcecQ77sJlaUi2RLyQeIugYlBuGe7BzboLvFPF3eybdFoh85082jdLnCTRtSpotzqFyH8KgBaR0S5w.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhS4lH8KDekgFMkvO6Sf22i5JpX5KMhUgL.FozNeh.RSK-01hM2dJLoI742qg4.9gpDdc4kMGHRIBtt; _T_WM=64517b8935f29e9c888d8b419a9e2cce; H5_INDEX=3; H5_INDEX_TITLE=Dandelion_puxi; SUB=_2A250D57qDeThGeRJ61sZ9SvPwzuIHXVX8yKirDV6PUJbkdBeLU3FkW045-nbFDQTs2pGcoVVU3eTvBSxVQ..; SUHB=04W_frWVc5eg-d; SSOLoginState=1493954234; M_WEIBOCN_PARAMS=featurecode%3D20000320%26luicode%3D10000011%26lfid%3D102803_ctg1_8999_-_ctg1_8999_home%26uicode%3D20000174'}
    HEADER = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}


    def __init__(self):
        pass

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, headers=self.HEADER, cookies=self.COOKIE)

    def create_urls(self):
        pass


    def __init__(self):
        pass

    def parse(self, response):
        print "body"
        print response.body
        pass
