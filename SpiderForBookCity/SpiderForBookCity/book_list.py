import requests
from lxml import etree
import pymysql
# class BookList(models.Model):
#     name = models.CharField(primary_key = True,max_length = 255) #书名
#     author = models.CharField(max_length = 255)                 #作者
#     read_num = models.CharField(max_length = 255)                  #阅读人数
#     book_type = models.ForeignKey(Category, models.DO_NOTHING)  #外键 ，书的类别

    # class Meta:
    #     db_table = "booklist"

def gethtml(url):
    try:
        headers = {'user-agent':'Mozilla/5.0'}
        r = requests.get(url, headers = headers)
        r.raise_for_status()
        r.encoding = 'gb2312'
        return r.text
    except:
        return ""

def parsepage(html):
    tree = etree.HTML(html)
    name = tree.xpath("/html/body/div[8]/ul//li/span[1]/a/b/text()")
    author = tree.xpath('/html/body/div[8]/ul//li/span[3]/text()')
    read_num = tree.xpath('/html/body/div[8]/ul//li/span[7]/text()')
    info = [name,author,read_num]
    return info

def connect_db(info, foreignkey_id):
    db = pymysql.connect("localhost",'root','1004210191','bookcity')
    cursor = db.cursor()
    for item in range(len(info[0])):
        sql = "insert into booklist(name, author, read_num, book_type_id) values('{}','{}','{}','{}')" \
            .format(info[0][item], info[1][item], info[2][item], foreignkey_id)
        # sql = 'update booklist'
        cursor.execute(sql)
        db.commit()

def main():
    url_list = ['https://www.x88dushu.com/sort{}/1/'.format(i) for i in range(1,9)]
    for url in range(1,len(url_list)+1):
        html = gethtml(url_list[url-1])
        info = parsepage(html)
        connect_db(info, url)
        print("{}存入数据库完毕".format(url))


if __name__ =="__main__":
    main()

# 每个分类的url

