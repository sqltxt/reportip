import urllib.request
import time
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

smtpserver = "smtp.163.com"
username = "sqltxt@163.com"
password = "iamanothwolf1999"
sender = "sqltxt@163.com"
receiver = ["sqltxt@qq.com"]
subject = "PI新IP"
#file_path = "/root/rootcrons/lastip.txt"
file_path = "C:\IP\lastip.txt"

def sendEmail(msghtml):
    msgRoot = MIMEMultipart('related')
    msgRoot["To"] = ','.join(receiver)
    msgRoot["From"] = sender
    msgRoot['Subject'] =  subject
    msgText = MIMEText(msghtml,'html','utf-8')
    msgRoot.attach(msgText)
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msgRoot.as_string())
    smtp.quit()
    
def getip():
    try:
        #myip = visit("http://ifconfig.me/")
        #myip = visit("http://www.ip.cn/")
        myip = visit("http://ip.chinaz.com/getip.aspx")
    except:
        try:
            myip = visit("http://2017.ip138.com/ic.asp")
        except:
            try:
                myip = visit("http://www.whereismyip.com/")
            except:
                print ("Fail to get the Network ip.")
                print ("Get the LAN ip.")
    return myip
    
def visit(url):
    print(url)
    response = urllib.request.urlopen(url,timeout=20)
    if url == response.geturl():
        str = response.read().decode("gbk")
        print(re.search('\d+\.\d+\.\d+\.\d+',str).group(0))
    return re.search('\d+\.\d+\.\d+\.\d+',str).group(0)

if __name__ == '__main__':
    while 1:
        ipaddr = getip() 
        print(ipaddr)
        ip_file = open(file_path)
        last_ip = ip_file.read()
        ip_file.close()
        print(last_ip)
        if last_ip == ipaddr:
            print ("IP not change.")
        else:
            print ("IP changed. New ip: {}".format(ipaddr))
            ip_file = open(file_path,"w")
            ip_file.write(str(ipaddr))
            ip_file.close()
            sendEmail(ipaddr)
            print ("Successfully send the e-mail.")
        time.sleep(3600)
