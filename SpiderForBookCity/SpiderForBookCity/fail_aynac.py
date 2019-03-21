# import asyncio
# import time

# import aiohttp
# import pymysql
# from bs4 import BeautifulSoup
# from scrapy.selector import Selector


# async def fetch(url):
#     headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
#          AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
#     async with asyncio.Semaphore(400):
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url, headers = headers) as resp:
#                 return await resp.text()

# async def parseurl(html,xpath_pat):
#     selector = Selector(text = html)
#     # url_xpath = '/html/body/div[8]/ul//li/a[@href]'
#     url_list = list(map(lambda x:"https://www.x88dushu.com/xiaoshuo/68/68289/"+x,selector.xpath(xpath_pat).extract()))
#     return url_list

# async def parsedetails(html):
#     # /html/body/div[5]/h1/text()
#     # /html/body/div[5]/div[4]//text()
#     soup=BeautifulSoup(html,'lxml')
#     a=soup.find('div',attrs={'class':"yd_text2"})   #找到储存在div标签下的章节内容
#     title=soup.find('h1')                           #找到标题所在的h1标签
#     return title.string,a.text

# async def main():
#     html = await fetch("https://www.x88dushu.com/xiaoshuo/110/110402/")
#     chapter_list = await parseurl(html, '/html/body/div[8]/ul//li/a/@href')
#     print(chapter_list)
#     lens = len(chapter_list)
#     for url in range(lens):
#         response = await fetch(chapter_list[url])
#         title,detail = await parsedetails(response)
#         print("总任务数为{}，执行到第{}个任务".format(lens,url))
#         print(time.time()-times)
#         if url%100 == 0 and url!=0:
#             time.sleep(3)
#         with open("D:/new.txt", "a", encoding="utf-8") as f:
#             f.write("/t/t/t/t/t{}/n{}".format(title,detail))

# if __name__ =="__main__":
#     loop = asyncio.get_event_loop()
#     print("开始下载")
#     times = time.time()
#     print(times)
#     loop.run_until_complete(main())
#     loop.close()
#     print("下载完毕,用时{}".format(time.time()-times))
