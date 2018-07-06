# dianping_crawler
爬取大众点评网信息
文件说明：
    shop_spider.py 爬取商店基础信息，通过食物分类和地点分类来构造url，获取每个范畴的首页信息，进而构造出其他分页信息

    location_foodType：存储店铺信息html文件

    behond_p1：存储待爬取的url

    crawled_url：存储已爬取的url

    shop_url：爬取的shop url

    shop：存储爬取到的url文件