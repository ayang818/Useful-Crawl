import requests
from bs4 import BeautifulSoup
import re

# URL = "https://api.bilibili.com/x/v1/dm/list.so?oid=103577530";
# 5f14db60

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
    UIDList = []
    for item in eval(UserIdMessage)["data"]:
        UIDList.append(item["id"])
    return UIDList

def searchCid(av):
    url = "https://www.bilibili.com/video/av"+str(av)
    text = getUrl(url)
    cid = re.findall("\"cid\":[0-9]{0,11},", text)[0].split(":")[1].split(",")[0]
    return cid

def writeFile(tempMessageList, av, isSearchUserID):
    with open("D:/Danmaku{}.txt".format(av), "w") as f:
        for (index, item) in enumerate(tempMessageList):
            try:
                if (isSearchUserID == "1"):
                    print("第{}条弹幕".format(index+1))
                f.write("-----------\n")
                f.write("第{}条弹幕\n".format(index))
                if (str(isSearchUserID) == "1"):
                    for UID in rehash(item["p"].split(",")[6]):
                        f.write("UID:" + str(UID) +"\n")
                else:
                    f.write("加密ID:"+item["p"].split(",")[6]+"\n")
                f.write(item.text+"\n")
            except:
                print("第{}条弹幕保存失败".format(index+1))
                pass
                
if __name__ == "__main__":
    av = input("请输入AV号 : ")
    isSearchUserID = input("请输入是否需要搜索用户ID，输入1表示是，其它表示否(此选项会大大降低运行速度) : ")
    print("正在保存，请稍等")
    try:
        writeFile(parseDOM(getApi(searchCid(av))), av, isSearchUserID)
        print("弹幕文件保存在 D:/Danmaku{}.txt".format(av))
        if (isSearchUserID != "1"):
            print()
    except:
        print("请确保输入了正确的av号，或检查网络连接是否正常")
