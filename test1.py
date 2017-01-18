#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2017/1/17.
# ---------------------------------
from threadspider.wk_spider import  *
import  time
from pyquery import  PyQuery
from gcutils.db import MySQLMgr
from threading  import  Lock
from selenium.webdriver.support.select import Select



mgr=MySQLMgr("192.168.8.94",3306,"shuili","root","gc895316")
lock=Lock()

spider_init(2,1000000)
for i in range(1,493):
    def handle(web,pagenum=i):
        time.sleep(2)
        _select=web.find_element_by_id("txt_1_sel")
        _select=Select(_select)
        _select.select_by_value("FT")
        web.execute_script('''jQuery("#txt_1_value1").attr("value","水沙变化")''')
        web.execute_script('''jQuery("#btnSearch").click()''')
        time.sleep(4)
        web.switch_to_frame("iframeResult")
        data= web.page_source
        doc=PyQuery(data)
        _url="http://kns.cnki.net/kns/brief/brief.aspx"+doc(".TitleLeftCell").find("a").attr("href")
        _url1=_url.replace("curpage=2","curpage=%s"%pagenum)#.replace("RecordsPerPage=20","RecordsPerPage=50")
        print _url1
        web.get(_url1)
        time.sleep(3)
        #from_url=_url1
        doc=PyQuery(web.page_source)
        for j in doc(".GridTableContent").find("tr[bgcolor]"):
            from_url=PyQuery(PyQuery(j).find("a")[0]).attr("href")
            from_url="http://kns.cnki.net"+from_url
            lock.acquire()
            for a,b,c,d,e,f in [PyQuery(j).find("td")[1:-2]]:
                title="".join([PyQuery(_).text() for _ in   PyQuery(a).find("a")]).replace(" ","")
                author=PyQuery(b).text()
                source=PyQuery(c).text().strip()
                publist_date=PyQuery(d).text().strip()
                if publist_date:
                    publist_date=publist_date.replace("/","-")
                else:
                    publist_date=""
                from_database="期刊"
                quote_times=PyQuery(e).find("a").text().strip()
                download_times=PyQuery(PyQuery(f).find("a")[-1]).text().strip()

                if quote_times:
                    quote_times=int(quote_times.strip())
                else:
                    quote_times=0
                if download_times:
                    download_times=int(download_times.strip())
                else:
                    download_times=0
                print title,author,source,"#",publist_date,"#",from_database,quote_times,download_times,from_url

                mgr.runOperation('''replace  into zhiwang_article_shuishabianhua_qikan_1( title, author, source, publist_date, source_database,
                                   quote_times, download_times, from_url)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''',
                                 (title,author,source,publist_date,from_database,quote_times,download_times,from_url))
            lock.release()
        web.delete_all_cookies()

    WkSpider("http://kns.cnki.net/kns/brief/result.aspx?dbprefix=CJFQ",handle=handle,force=True)
spider_join()