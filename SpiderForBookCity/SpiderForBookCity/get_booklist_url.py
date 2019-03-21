#这是爬取列表下所有书籍的总目录
import requests
from scrapy.selector import Selector
import pymysql
import process_ban_bookdetails as pb
import time
from multiprocessing import Process

def main():
    type_list = ["https://www.x88dushu.com/sort{}/1/".format(i) for i in range(1,9)]
    for url_id in range(len(type_list)):
        # /html/body/div[8]/ul/li[2]/span[1]/a
        html = pb.getHTML(type_list[url_id])
        selector = Selector(text=html)
        url_list = list(map(lambda x:type_list[url_id] + x,\
            selector.xpath("/html/body/div[8]/ul//li/span[1]/a/@href").extract()))
        for url in url_list:
            ulist = pb.geturllist(url)
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

if __name__ =="__main__":
    main()