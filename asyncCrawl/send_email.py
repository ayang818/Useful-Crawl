import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

mail_host = 'smtp.qq.com'
port = 465
send_by = 'ayang818@qq.com'
password = '开启SMTP服务后，QQ邮箱自动生成的16位密码'
send_to = 'ayang818@qq.com'

def send_email(title,content,fileaddress):
    message = MIMEMultipart()
    message["From"] = send_by
    message['To'] = send_to
    message['Subject'] = title
    message.attach(MIMEText(content,'plain','utf-8'))
    #下面是发送附件类
    try:
        with open(fileaddress,'r',encoding = 'utf-8') as f:
            mime = MIMEBase('text','txt',filename = fileaddress)
            mime.add_header('Content-Disposition','321',filename = fileaddress)
            mime.set_payload(f.read())
            message.attach(mime)
    except:
        pass
    # print(message)
    try:
        #要注意位置参数和关键字参数啊啊
        smpt = smtplib.SMTP_SSL(mail_host, port, 'utf-8')
        smpt.login(send_by,password)
        smpt.sendmail(send_by, send_to,message.as_string(),)
        # print(message.as_string)
        smpt.quit()
        print("发送成功")
    except:
        print("发送失败")

if __name__ == "__main__":
    title = '附件文件测试'
    content = '三体'
    # title:标题 ， context:正文 ，第三个参数选填
    send_email(title, content, "D:/三体.txt")
--------------------- 
作者：六月的想象 
来源：CSDN 
原文：https://blog.csdn.net/weixin_43434223/article/details/89047311 
版权声明：本文为博主原创文章，转载请附上博文链接！
