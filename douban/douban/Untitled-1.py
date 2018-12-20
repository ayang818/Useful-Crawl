from  PIL import Image
from io import BytesIO
import requests
r=requests.get('https://www.douban.com/misc/captcha?id=pFmvnxW6ak7zOYYCUS7gjbY9:en&size=s')
img=Image.open(BytesIO(r.content))
img.show()
captcha=input('输入验证码:')
img.close()
print(captcha)