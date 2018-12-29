'''
项目解析:利用https://www.x88dushu.com/这个网站的图书资源进行解析爬取
技术路径:requests库，Beautiful库，re库
实现方法:1.向网站主页面的url加入要搜索的图书信息元素，构造搜索图书页面的url，并在搜索图书页面解析获得目标图书的url。
        2.访问目标图书的url，解析页面，获得图书各个章节的url链接，构造列表。
        3.遍历列表中的各个章节url，解析页面获得图书内容。
        4.将获得的图书内容写入一个txt文件中。
2018.12.13日:第一次修改,完成搜索图书的功能
2018.12.16日:第二次修改,1.添加可视化的进度条。
                       2.解决没有图书导致的报错。
                       3.给程序添加了结束端口。
'''
import requests
from bs4 import BeautifulSoup
import re
import os
import time
from tqdm import tqdm
print('TIPS1：请保持网络状态良好哦。')
#在网站的搜索栏里进行搜索，找出书籍目录的url链接xzcz
def searchurl(url,dicts):
    try:
        r=requests.get(url,params=dicts,headers={'user-agent':'Mozilla/5.0'})
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        print('访问搜索小说页面成功')
    except:
        print('访问搜索页面失败')
    try:
        soup=BeautifulSoup(r.text,'lxml')
        bookurl=soup.find('p')                      #解析html页面发现目标书籍的对应url保存在一个/p/a标签中
        bookurl=bookurl.find('a')['href']           #找到p标签中的a标签，提取目标书籍页面的url
        return bookurl
    except:
        print('没有找到对应的书籍。')                                                   
   
    
#访问目录书籍的url，解析页面获得各个章节的url链接，形成列表
def geturllist(url,ulist):
    try:
        r=requests.get(url)                     
        r.raise_for_status()
        r.encoding=r.apparent_encoding
    except:
        print('下载失败')
    try:
        soup=BeautifulSoup(r.text,'lxml')
        lista=soup.find_all('a',attrs={'href':re.compile(r'\d+\.html')})    #利用re库找到带有每个章节url的属性的a标签
        lista=lista[1:]                                                     #解析发现构造的列表中第一个和第二个url是无用的
        for i in lista:
            ulist.append(i['href'])
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
        title=soup.find('h1')                           #找到标题所在的h1标签
        return [a.text,title.string]                    #以列表形式返回内容
    except:
        return ''
   
#对读取到的章节标题和章节内容进行文件的写入
def writefile(text,title):
    try:
        with open('D:/'+title+'.txt','a',encoding='utf-8') as f:            #使用utf-8编码方式写入文件
            f.write('\t\t\t\t\t\t\t\t\t\t'+text[1]+'\n\n\n'+text[0])        #\t为了标题居中，\n标题与内容间换行
    except:
        return ''
        
#主函数
def main():
    url='https://so.x88dushu.com/search/so.php?search_field=0'
    title=str(input('(请输入正确且完整的小说名)输入小说名:'))
    time1=time.time()
    data={'q':title}     #作为params参数进行目标图书的搜索
    ulist=[]             #用于获取目录url列表
    usefulurl=searchurl(url,data)   
    geturllist(usefulurl,ulist)
    a=0                  #计数
    for i in tqdm(ulist,ncols=100):
        aurl=usefulurl+'/'+i        #每个章节网页的url是目标图书url+ulist中的后缀，后缀例如12345.html
        html=getHTML(aurl)          
        text=parsepage(html)
        writefile(text,title)
        a+=1      
    if a!=0:
        print('-----'*2)
        print('下载完毕')
        print('文件保存在D:/'+title+'.txt')
        print('用了',time.time()-time1,'秒')
        print('^-^')
        print('-----'*2)
    label=input('如果想继续下载请按1,若不想请按2:')
    if int(label)==1:
        main()

if __name__=='__main__':   
    main()


        
