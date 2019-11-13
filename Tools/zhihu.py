import requests
from lxml import etree 

# 知乎热榜爬虫示例
url = "https://www.zhihu.com/hot"
headers = {"User-Agent": "Mozilla/5.0", "Cookie": '替换成你自己的Cookie'}
response = requests.get(url, headers = headers)
response.encoding = response.apparent_encoding
tree = etree.HTML(response.text)
title = tree.xpath('//*[@id="TopstoryContent"]/div/div/div[2]//section/div[2]/a/h2')
for item in title:
    print(item.text)