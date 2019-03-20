import requests
from lxml import etree
import pymysql

def gethtml(url):
    try:
        headers = {'user-agent':'Mozilla/5.0'}
        r = requests.get(url, headers = headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def parsepage(html):
    tree = etree.HTML(html)
    categary_list1 = tree.xpath("/html/body/div[6]//ul/li[1]/h2/a/text()")
    categary_list2 = tree.xpath("/html/body/div[7]//ul/li[1]/h2/a/text()")
    categary_list = categary_list1 + categary_list2
    return categary_list

def connect_db(categary_list):
    db = pymysql.connect("localhost",'root','1004210191','bookcity')
    cursor = db.cursor()
    for item in range(len(categary_list)):
        sql = "insert into category(id, type_name) values('{}','{}');".format(item+1 , categary_list[item])
        cursor.execute(sql)
        db.commit()


def main():
    url = 'https://www.x88dushu.com/'
    html = gethtml(url)
    result = parsepage(html)
    connect_db(result)
    print("类别分类完成")


if __name__ =="__main__":
    main()


# class Category(models.Model):
#     id = models.CharField(primary_key = True,max_length = 255)
#     type_name = models.CharField(max_length = 255)

#     class Meta:
#         db_table = "category"

