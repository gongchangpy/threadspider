#coding:utf-8
# write  by  zhou

from threadspider.http_spider import  *
import pyquery
import gzip
from StringIO import  StringIO
import pymongo
import sys
import re
reload(sys)
sys.setdefaultencoding("utf-8")

req={}
req["User-Agent"] = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36'
req["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
req["Accept-Encoding"] = "gzip, deflate"
req["Accept-Language"] = "zh-CN,zh;q=0.9,en;q=0.8"
req["Upgrade-Insecure-Requests"]="1"
req["Cache-Control"]="max-age=0"
spider_init(100)

mongo_client = pymongo.MongoClient("192.168.8.137",27017)
db = mongo_client["zkptest"]

def res_handle(res):
    buf = StringIO(res)
    f = gzip.GzipFile(fileobj=buf)
    res = f.read().decode("utf-8",errors="ignore").encode("utf-8")
    doc = pyquery.PyQuery(res)
    for i in doc("a"):
        href = pyquery.PyQuery(i).attr("href")
        if href and  "huangye88.com"  in href:
            if re.search("/xinxi/\d+\.html.*?",href):
                Spider(href,headers=req,response_handle=get_detail_handle(href),retry_times=3)
            else:
                Spider(href,headers=req,response_handle=res_handle,retry_times=3)


def get_detail_handle(url):
    def detail_handle(res):
        buf = StringIO(res)
        f = gzip.GzipFile(fileobj=buf)
        res = f.read().decode("utf-8",errors="ignore").encode("utf-8")
        try:
            db["huangye88"].insert({"_id":url,"html":res})
        except:
            pass
        doc = pyquery.PyQuery(res)
        print "write mongo"
        for i in doc("a"):
            href = pyquery.PyQuery(i).attr("href")
            if href and  "huangye88.com"  in href:
                if re.search(r"/xinxi/\d+\.html.*?",href):
                    Spider(href,headers=req,response_handle=get_detail_handle(href),retry_times=3)
                else:
                    Spider(href,headers=req,response_handle=res_handle,retry_times=3)
    return  detail_handle

Spider("http://www.huangye88.com",response_handle=res_handle,headers=req,retry_times=3)
spider_join()