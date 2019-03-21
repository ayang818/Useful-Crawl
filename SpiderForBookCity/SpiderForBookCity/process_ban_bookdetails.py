import requests
from bs4 import BeautifulSoup
import re
import os
import time
from scrapy.selector import Selector
from multiprocessing import Process

def geturllist(url):
    try:
        r=requests.get(url)                     
        r.raise_for_status()
        r.encoding=r.apparent_encoding
    except:
        print('下载失败')
    try:
        selector = Selector(text= r.text)
        ulist = list(map(lambda a:url+a,selector.xpath("/html/body/div[8]/ul//li/a/@href").extract()))
        return ulist
    except:
        return ''

#得到各个章节的html文本
def getHTML(url):
    try:
        r=requests.get(url)
        r.raise_for_status
        r.encoding=r.apparent_encoding        
        return r.text
    except:
        print('解析页面失败')
        return ''
    
#解析章节的html文本，得到章节标题和章节内容
def parsepage(html):
    try:
        soup=BeautifulSoup(html,'lxml')
        a=soup.find('div',attrs={'class':"yd_text2"})   #找到储存在div标签下的章节内容
        title=soup.find('h1')                    #找到标题所在的h1标签
        return title.string,a.text                    #以列表形式返回内容
    except:
        return ''

  
#对读取到的章节标题和章节内容进行文件的写入
def writefile(title,text):
    try:
        with open('D:/'+"英雄时刻/"+title+'.txt','a',encoding='utf-8') as f:            #使用utf-8编码方式写入文件
            f.write('\t\t\t\t\t\t\t\t\t\t'+text+'\n\n\n')        #\t为了标题居中，\n标题与内容间换行
    except:
        return ''

def main(lists,i):
    for url in lists:
        html = getHTML(url)
        title,context = parsepage(html)
        # print(title)
        writefile(title,context)
        print("任务{}下载中".format(i))
    print("任务结束")

if __name__ == "__main__":
    url = "https://www.x88dushu.com/xiaoshuo/116/116123/"
    ulist = geturllist(url)
    print(len(ulist))
    lens = len(ulist)//8
    tasks = []
    list1 = ulist[:lens]
    list2 = ulist[lens:2*lens]
    list3 = ulist[2*lens:3*lens]
    list4 = ulist[3*lens:4*lens]
    list5 = ulist[4*lens:5*lens]
    list6 = ulist[5*lens:6*lens]
    list7 = ulist[6*lens:7*lens]
    list8 = ulist[7*lens:]
    tasks = [list1,list2,list3,list4,list5,list6,list7,list8]
    processes = []
    time_start = time.time()
    for i in range(len(tasks)):
        print(i)
        process = Process(target = main,args= (tasks[i],i,))
        processes.append(process)
    for process in processes:
        process.start()
    

    







