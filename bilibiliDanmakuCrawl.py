import requests
from bs4 import BeautifulSoup
import re

# URL = "https://api.bilibili.com/x/v1/dm/list.so?oid=103577530";

def getUrl(url):
    res = requests.get(url, headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"})
    res.encoding = res.apparent_encoding
    res = res.text
    return res

def getApi(cid):
    url = "https://api.bilibili.com/x/v1/dm/list.so?oid="+str(cid)
    dmXMLtext = getUrl(url)
    return dmXMLtext

def parseDOM(text):
    soup = BeautifulSoup(text, "xml")
    dmList = soup.find_all("d")
    return dmList

def rehash(hashedID):
    UserIdMessage = getUrl("https://biliquery.typcn.com/api/user/hash/"+hashedID)
    return eval(UserIdMessage)["data"][0]["id"]

def searchCid(av):
    url = "https://www.bilibili.com/video/av"+str(av)
    text = getUrl(url)
    cid = re.findall("\"cid\":[0-9]{0,11},", text)[0].split(":")[1].split(",")[0]
    return cid

def writeFile(tempMessageList, av):
    i = 1
    with open("D:/Danmaku{}.txt".format(av), "a") as f:
        for item in tempMessageList:
            try:
                f.write("-----------\n")
                f.write("第{}条弹幕\n".format(i))
                # f.write("用户ID : " + str(rehash(item["p"].split(",")[6])) +"\n")
                f.write(item.text+"\n")
            except:
                print("第{}条弹幕保存失败".format(i))
                pass
            finally:
                i+=1

if __name__ == "__main__":
    av = input("请输入AV号 : ")
    print("正在保存，请稍等")
    writeFile(parseDOM(getApi(searchCid(av))), av)
    print("弹幕文件保存在 D:/Danmaku{}.txt".format(av))