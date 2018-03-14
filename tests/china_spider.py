# coding:utf-8
# write  by  zhou

from threadspider.http_spider import *
import pyquery
import pymongo
import sys
import re

reload(sys)
sys.setdefaultencoding("utf-8")

# headers伪装
headers = {}
headers["User-Agent"] = 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html'

# 爬虫线程池初始化
spider_init(20)

mongo_client = pymongo.MongoClient("192.168.8.137", 27017)
db = mongo_client["zkptest"]


# 首页及相关聚合页处理函数
def res_handle(res):
    doc = pyquery.PyQuery(res)
    for i in doc("a"):
        href = pyquery.PyQuery(i).attr("href")
        if href and "site.china.cn" in href:
            if re.search(r"site.china.cn/[a-z]+/\d+\.html.*?", href):
                href = href.split("?")[0]
                Spider(href, headers=headers, response_handle=get_detail_handle(href), retry_times=3, charset="gbk",
                       priority=3)  # 爬取详情
            else:

                href = href.split("?")[0]
                Spider(href, headers=headers, response_handle=res_handle, retry_times=3, charset="gbk") # 爬取聚合页

# 详情页处理函数
def get_detail_handle(url):
    def detail_handle(res):
        try:
            db["china"].insert({"_id": url, "html": res})
        except:
            pass
        doc = pyquery.PyQuery(res)
        print "write mongo"
        for i in doc("a"):
            href = pyquery.PyQuery(i).attr("href")
            if href and "site.china.cn" in href:
                if re.search(r"site.china.cn/[a-z]+/\d+\.html.*?", href):
                    href = href.split("?")[0]
                    Spider(href, headers=headers, response_handle=get_detail_handle(href), retry_times=3, charset="gbk",
                           priority=3)
                else:

                    href = href.split("?")[0]
                    Spider(href, headers=headers, response_handle=res_handle, retry_times=3, charset="gbk")

    return detail_handle


Spider("https://site.china.cn/", response_handle=res_handle, headers=headers, retry_times=3, charset="gbk")  # 爬虫入口页面
spider_join()  # 等待爬虫执行完成
