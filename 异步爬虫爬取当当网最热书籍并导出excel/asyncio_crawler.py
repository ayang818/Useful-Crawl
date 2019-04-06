import asyncio
import time
from multiprocessing import Process

import aiohttp
import numpy as np
import pandas as pd
import requests
from scrapy.selector import Selector
from tqdm import tqdm

async def gethtml(url, dicts):
    async with aiohttp.ClientSession() as session:
        # params = r"ddscreen=2; dest_area=country_id%3D9000%26province_id%3D111%26city_id%20%3D0%26district_id%3D0%26town_id%3D0; __permanent_id=20190405214132382691121618569658467; __rpm=...1554472832829%7C...1554472838493; __visit_id=20190405224707728341459953194932707; __out_refer=; __trace_id=20190405225132217370180800638424217"
        # params.
        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
            }
        cookies = {"cookies_are":dicts}
        async with session.get(url, headers = headers, cookies = cookies) as res:
            # print(await res.text())
            try:
                return await res.text('gb2312')
            except:
                return ""

async def parse(texts):
    selector = Selector(text = texts)
    css_for_title = 'body > div.bang_wrapper > div.bang_content > div.bang_list_box > ul li > div.name > a::text'
    css_for_author = 'body > div.bang_wrapper > div.bang_content > div.bang_list_box > ul li > div:nth-child(5) > a:nth-child(1)::text'
    css_for_price = 'body > div.bang_wrapper > div.bang_content > div.bang_list_box > ul li > div.price > p:nth-child(1) > span.price_n::text'
    titles = selector.css(css_for_title).extract()
    authors = selector.css(css_for_author).extract()
    prices = selector.css(css_for_price).extract()
    return [titles, authors, prices]

async def main(url):
    # print(url_list)
    global icon
    icon = 1
    params = r"ddscreen=2; LOGIN_TIME=1554477709575; dest_area=country_id%3D9000%26province_id%3D111%26city_id%20%3D0%26district_id%3D0%26town_id%3D0; __permanent_id=20190405214132382691121618569658467; __visit_id=20190405224707728341459953194932707; __out_refer=; permanent_key=20190405232032240182889951b7f8e2; __rpm=login_page.login_password_div..1554477638469%7Clogin_share_bind_page...1554477708199; USERNUM=9k+wlGHtJmDpgx3V9fNOIA==; login.dangdang.com=.AYH=20190405232138043884709&.ASPXAUTH=H6JEeCLpLDkmMbb6j/xtACG1AULA4xr7xHRQDeCdj7ZIgM3G5eBykg==; dangdang.com=email=MTk5NzUyNjAxOTE1ODE1OEBkZG1vYmlscGhvbmVfX3VzZXIuY29t&nickname=&display_id=9341043676724&customerid=dzoyKRWFYdyI8gvrxuN36Q==&viptype=kXDbk8oIyG0=&show_name=199%2A%2A%2A%2A0191; ddoy=email=1997526019158158%40ddmobilphone__user.com&nickname=&agree_date=1&validatedflag=0&uname=19975260191&utype=&.ALFG=off&.ALTM=1554477708; sessionID=pc_33efdf47b8e4eff005e19cc13b74fffd9cabe44a000313acddd1672306adb00b; __dd_token_id=20190405232148632665868446bf7335; order_follow_source=-%7C-O-123%7C%2311%7C%23login_third_qq%7C%230%7C%23; __trace_id=20190405232149589371503745904925594"
    # d = {}
    # params = params.split("; ")
    # for item in params:
    #     rest = item.split("=")
    #     d[rest[0]] = rest[1]
    response = await gethtml(url, params)
    try:
        result = await parse(response)
        data = {
            '书名':result[0],
            '作者':result[1],
            '价格':result[2],
        }
        one_page_msg = pd.DataFrame(data, index = [i for i in range(1,21)])
        # if url == 1: 
        one_page_msg.to_excel("D:/book_data_new{}.xlsx".format(icon),sheet_name="sheet 1",encoding='utf-8')
        # else:
        #     one_page_msg.to_excel("D:/book_data_new.xlsx",sheet_name="sheet 1",encoding='utf-8')
        print("页面{}爬取成功".format(icon))
        icon += 1
    except:
        print("页面{}保存失败".format(icon))
        icon += 1

if __name__ == "__main__":
    url_list = ["http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent7-0-0-1-{}".format(i) for i in range(1,26)]
    start_time = time.time()
    print("开始爬取")
    loop = asyncio.get_event_loop()
    # maps = map(lambda main : main(), url_list)
    maps = []
    for url in url_list:
        maps.append(main(url))
    loop.run_until_complete(asyncio.wait(maps))
    loop.close()
    print("爬取结束，用时 {}s".format(time.time()-start_time))
    