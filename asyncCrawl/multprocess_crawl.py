import time
from multiprocessing import Process

import pandas as pd
import requests
from scrapy.selector import Selector


def main(url,icon):
    print("下载任务{}".format(icon))

    r = requests.get(url,headers = {"user-agent":"Mozilla/5.0"})
    r.encoding = r.apparent_encoding
    selector = Selector(text=r.text)
    css_for_title = 'body > div.bang_wrapper > div.bang_content > div.bang_list_box > ul li > div.name > a::text'
    css_for_author = 'body > div.bang_wrapper > div.bang_content > div.bang_list_box > ul li > div:nth-child(5) > a:nth-child(1)::text'
    css_for_price = 'body > div.bang_wrapper > div.bang_content > div.bang_list_box > ul li > div.price > p:nth-child(1) > span.price_n::text'
    titles = selector.css(css_for_title).extract()
    authors = selector.css(css_for_author).extract()
    prices = selector.css(css_for_price).extract()
    try:
        data = {
            "书名":titles,
            "作者":authors,
            "价格":prices,
        }
        df = pd.DataFrame(data, index = [i for i in range(1,21)])
        df.to_excel("D:/process_version_popular_book{}.xlsx".format(icon),encoding=r.apparent_encoding)
        print("任务{}下载完毕".format(icon))
    except:
        print("任务{}下载失败".format(icon))

if __name__ == "__main__":    
    url_list = ["http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent7-0-0-1-{}".format(i) for i in range(1,26)]
    start_time = time.time()    
    for i in  range(len(url_list)):
        pro = Process(target = main, args = (url_list[i],i,))
        pro.start()

    
