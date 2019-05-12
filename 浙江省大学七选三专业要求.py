import requests
from lxml import etree
from bs4 import BeautifulSoup
import pandas as pd


def gethtml(url):
    try:
        splash_url = "http://ayang818.top:8050/render.html"
        args = {"url":url,"timeout":5}
        headers = {"user-agent":"Mozilla/5.0"}
        r = requests.get(splash_url, headers = headers,params=args)
        r.encoding = "utf-8"
        # print(r.text)
        # print("正在爬取界面")
        return r.text
    except:
        return False

def parseChioceUrl(tex):
    tree = etree.HTML(text = tex)
    href = tree.xpath('//*[@id="dis_1"]/table[2]/tbody//tr/td[2]/text()')
    return href

def parseOneSchool(tex, schoolID):
    try:
        tree = etree.HTML(text = tex)
        level = tree.xpath("/html/body/div/div[2]/div/div[2]/table/tbody//tr/td[1]/text()")
        # print(level)
        # print(len(level))
        name = tree.xpath("/html/body/div/div[2]/div/div[2]/table/tbody//tr/td[2]/text()")
        # print(name)
        # print(len(name))
        number = tree.xpath("/html/body/div/div[2]/div/div[2]/table/tbody//tr/td[3]/text()")
        # print(number)
        # print(len(number))
        ranges = tree.xpath("/html/body/div/div[2]/div/div[2]/table/tbody//tr/td[4]/text()")
        # print(ranges)
        # print(len(ranges))
        redis = pd.read_excel("D:/message.xlsx")
        data = {
            "ID":schoolID,
            "层次": level,
            "专业(类)名称":name,
            "选考科目数":number,
            "选考科目范围":ranges,
        }
        df = pd.DataFrame(data)
        print(df)
        print(redis)
        final_data = pd.concat([redis, df])
        # print(final_data)
        final_data.to_excel("D:/message.xlsx",index=False)
    except:
        pass

BASE_URL = "http://zt.zjzs.net/xuanke2018/"
url1 = ["http://zt.zjzs.net/xuanke2018/area_0_{}.html".format(x) for x in range(0,12)]
url2 = ["http://zt.zjzs.net/xuanke2018/area_1_{}.html".format(x) for x in range(0,12)]
url3 = ["http://zt.zjzs.net/xuanke2018/area_2_{}.html".format(x) for x in range(0,7)]
# print(url1, url2, url3)
final_url_list = url1+url2+url3
for url in final_url_list:
    text = gethtml(url)
    IDList = parseChioceUrl(text)
    # print(IDList)
    for next_url in IDList:
        targeturl = BASE_URL+next_url+".html"
        print(targeturl)
        response = gethtml(targeturl)
        parseOneSchool(response, next_url)
        print("正在爬取编号为{}的学校".format(next_url))



