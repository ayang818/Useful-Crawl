import asyncio
import aiohttp
import requests
from lxml import etree
from scrapy.selector import Selector
import pymysql
import time


async def gethtml(url):
    headers = {'User-Agent':"Mozilla/5.0"}
    # async with asyncio.Semaphore(8):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers = headers) as response:
            html = await response.text()
            print(html)
            print("---------------------")


loop = asyncio.get_event_loop()
book_list = ['https://www.x88dushu.com/sort{}/1/'.format(i) for i in range(1,9)]
tasks = [gethtml(url) for url in book_list]
timenow = time.time()
loop.run_until_complete(asyncio.wait(tasks))
print("it cost {}".format(time.time()- timenow))
loop.close()



