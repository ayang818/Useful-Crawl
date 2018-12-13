import requests
from bs4 import BeautifulSoup
import re
import os

#在网站的搜索栏里进行搜索，找出书籍目录的url链接
def searchurl(url,dicts):
    try:
        r=requests.get(url,params=dicts,headers={'user-agent':'Mozilla/5.0'})
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        print('爬取搜索小说页面成功')
    except:
        print('爬取搜索页面失败')
    soup=BeautifulSoup(r.text,'html.parser')
    bookurl=soup.find('p')
    bookurl=bookurl.find('a')['href']    
    return bookurl
    

def geturllist(url,ulist):
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        print('爬取成功')
    except:
        print('爬取失败')
    soup=BeautifulSoup(r.text,'html.parser')
    lista=soup.find_all('a',attrs={'href':re.compile(r'\d+\.html')})
    lista=lista[1:]
    
    for i in lista:
        ulist.append(i['href'])
    return ulist

def getHTML(url):
    try:
        r=requests.get(url)
        r.raise_for_status
        r.encoding=r.apparent_encoding 
        print("解析页面成功")       
        return r.text
    except:
        print('解析页面失败')
        return ''
    

def parsepage(html):
    
    soup=BeautifulSoup(html,'html.parser')
    a=soup.find('div',attrs={'class':"yd_text2"})
    title=soup.find('h1')    
    return [a.text,title.string]
   

def writefile(text,title):
    with open('D:/'+title+'.txt','a',encoding='utf-8') as f:
        f.write('\t\t\t\t\t\t\t\t\t\t'+text[1]+'\n\n\n'+text[0])

def main():
    url='https://so.x88dushu.com/search/so.php?search_field=0'
    title=str(input('输入小说名:'))
    data={'q':title}
    ulist=[]
    usefulurl=searchurl(url,data)
    geturllist(usefulurl,ulist)

    for i in ulist:
        aurl=usefulurl+'/'+i
        html=getHTML(aurl)
        text=parsepage(html)
        writefile(text,title)       
        print('正在爬取')
    print('下载完毕')

main()



        