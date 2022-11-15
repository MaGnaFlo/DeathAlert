import smtplib
import json


jFilePath = "../infos/infos.json"


jFile = open(jFilePath, 'r')
	
jObj = json.load(jFile)

sender = jObj["user"]["address"]
pwd = jObj["user"]["password"]
receiver = jObj["receiver"]["address"]
server = jObj["SMTP"]["server"]
port = int(jObj["SMTP"]["port"])

msg = "hello!"

session = smtplib.SMTP(server, port)
session.starttls()

print('login')
session.login(sender, pwd)

print('send mail')
session.sendmail(sender, receiver, msg)
session.quit()
