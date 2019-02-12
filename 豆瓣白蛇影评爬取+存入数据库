import time

import pymysql
import requests
from lxml import etree


def gethtml(url):
    headers = {"user-agent":"Mozilla\5.0","cookie" :'ll="108298"; bid=xvnl6vQrv9o; _ga=GA1.2.1575037160.1545221946; __utmv=30149280.18889; ue="1004210191@qq.com"; douban-fav-remind=1; __yadk_uid=Uv3cySjO5gLWoaLcL121fhDAax80eQ8k; _vwo_uuid_v2=DAF8EEE77D1E24172A50ECAA433F53066|8c5a59ff92a7bff5e3aa313261b31b46; __utma=30149280.1575037160.1545221946.1548676993.1549172636.8; __utmc=30149280; __utmz=30149280.1549172636.8.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ap_v=0,6.0; __utmb=30149280.2.10.1549172636; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1549172650%2C%22https%3A%2F%2Fwww.douban.com%2Fsearch%3Fq%3D%25E7%2599%25BD%25E8%259B%2587%25E7%25BC%2598%25E8%25B5%25B7%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.1575037160.1545221946.1548676993.1549172650.2; __utmb=223695111.0.10.1549172650; __utmc=223695111; __utmz=223695111.1549172650.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; _pk_id.100001.4cf6=c6bde1212b80e918.1548676996.2.1549172669.1548677229.'}
    try:
        r = requests.get(url, headers = headers)
        r.raise_for_status()
        return r.text
    except:
        print("error")

def parsepage(html,ulist):
    tree = etree.HTML(html)
    name = tree.xpath('//*[@id="comments"]//div/div[2]/h3/span[2]/a/text()')
    view = tree.xpath('//*[@id="comments"]//div/div[2]/p/span/text()')
    for i in range(len(name)):
        ulist.append([name[i], view[i]])
    return ulist
        
def connect_pymysql(ulist,db):
    cursor = db.cursor()
    for item in ulist:
        sql = "insert into white_snack(name,view) values('%s','%s');" %(item[0],item[1])
        cursor.execute(sql)
        db.commit()

def main():
    urls = ["https://movie.douban.com/subject/30331149/comments?start={}&limit=20&sort=new_score&status=P".format(str(i)) for i in range(0,201,20)]
    ulist =[]
    db = pymysql.connect("localhost","root","1004210191","spider")
    cursor = db.cursor()
    for url in urls:
        html = gethtml(url)
        ulist = parsepage(html,ulist)
        connect_pymysql(ulist,db)
        time.sleep(2)        
    print("记录完成")
    db.close()
    print("\a")

main()
