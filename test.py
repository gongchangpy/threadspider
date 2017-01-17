#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2017/1/17.
# ---------------------------------
from threadspider.wk_spider import  *

spider_init(2,1000000)
for i in range(1,493):
    def handle(web,pagenum=i):
        print web.page_source
    WkSpider("http://kns.cnki.net/kns/brief/Default_Result.aspx?code=CJFQ&kw=%E6%B0%B4%E6%B2%99%E5%8F%98%E5%8C%96&korder=0&sel=1",handle=handle,force=True)
spider_join()