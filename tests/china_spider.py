# coding:utf-8
# write  by  zhou

from threadspider.http_spider import *
import pyquery
import pymongo
import sys
import re

reload(sys)
sys.setdefaultencoding("utf-8")

headers = {}
headers["User-Agent"] = 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html'

spider_init(20)

mongo_client = pymongo.MongoClient("192.168.8.137", 27017)
db = mongo_client["zkptest"]


def res_handle(res):
    doc = pyquery.PyQuery(res)
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


Spider("https://site.china.cn/", response_handle=res_handle, headers=req, retry_times=3, charset="gbk")
spider_join()
