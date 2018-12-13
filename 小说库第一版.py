'''
项目解析:利用https://www.x88dushu.com/这个网站的图书资源进行解析爬取
技术路径:requests库，Beautiful库，re库
实现方法:1.向网站主页面的url加入要搜索的图书信息元素，构造搜索图书页面的url，并在搜索图书页面解析获得目标图书的url。
        2.访问目标图书的url，解析页面，获得图书各个章节的url链接，构造列表。
        3.遍历列表中的各个章节url，解析页面获得图书内容。
        4.将获得的图书内容写入一个txt文件中。
2018.12.13日:第一次修改，完成搜索图书的功能
'''
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
    bookurl=soup.find('p')                      #解析html页面发现目标书籍的对应url保存在一个/p/a标签中
    bookurl=bookurl.find('a')['href']           #找到p标签中的a标签，提取目标书籍页面的url
    return bookurl
    
#访问目录书籍的url，解析页面获得各个章节的url链接，形成列表
def geturllist(url,ulist):
    try:
        r=requests.get(url)                     
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        print('爬取成功')
    except:
        print('爬取失败')
    soup=BeautifulSoup(r.text,'html.parser')
    lista=soup.find_all('a',attrs={'href':re.compile(r'\d+\.html')})    #利用re库找到带有每个章节url的属性的a标签
    lista=lista[1:]                                                     #解析发现构造的列表中第一个和第二个url是无用的
    for i in lista:
        ulist.append(i['href'])
    return ulist

#得到各个章节的html文本
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
    
#解析章节的html文本，得到章节标题和章节内容
def parsepage(html):
    soup=BeautifulSoup(html,'html.parser')
    a=soup.find('div',attrs={'class':"yd_text2"})   #找到储存在div标签下的章节内容
    title=soup.find('h1')                           #找到标题所在的h1标签
    return [a.text,title.string]                    #以列表形式返回内容
   
#对读取到的章节标题和章节内容进行文件的写入
def writefile(text,title):
    with open('D:/'+title+'.txt','a',encoding='utf-8') as f:            #使用utf-8编码方式写入文件
        f.write('\t\t\t\t\t\t\t\t\t\t'+text[1]+'\n\n\n'+text[0])        #\t为了标题居中，\n标题与内容间换行
#主函数
def main():
    url='https://so.x88dushu.com/search/so.php?search_field=0'
    title=str(input('输入小说名:'))
    data={'q':title}     #作为params参数进行目标图书的搜索
    ulist=[]             #用于获取目录url列表
    usefulurl=searchurl(url,data)   
    geturllist(usefulurl,ulist)
    for i in ulist:
        aurl=usefulurl+'/'+i        #每个章节网页的url是目标图书url+ulist中的后缀，后缀例如12345.html
        html=getHTML(aurl)          
        text=parsepage(html)
        writefile(text,title)       
        print('正在爬取')           #以示在运行^-^
    print('下载完毕')

main()



        