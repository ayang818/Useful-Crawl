import requests
from lxml import etree
import time
from multiprocessing import Process,Pool

#多进程好像逐渐要把函数合并了哎
def main(url):
    html = requests.get(url)
    html.encoding = 'gb2312'
    data = etree.HTML(html.text)
    title = data.xpath('//a[@class="ulink"]/text()')
    summary = data.xpath('//td[@colspan="2"]/text()')
    urls = data.xpath('//a[@class="ulink"]/@href')
    for t,s,u in zip(title,summary,urls):
        print(t)
        url_url = '【url:】http://www.dytt8.net'+u
        intro = '【简介】>>>>>>>'+s
        print(url_url)
        print(intro)
        with open("D:/linshi1.txt",'a') as f:
            f.write("-----------",url_url+"/n"+intro,"-----------")

if __name__ == '__main__':
    start = time.time()
    url = 'http://www.dytt8.net/html/gndy/dyzz/'
    pg_url = [url+'list_23_{}.html'.format(str(x)) for x in range(1,10)]
    p = Pool(8)
    p.map(main, pg_url)
    end = time.time()
    print("共计用时%.4f秒"%(end-start))
