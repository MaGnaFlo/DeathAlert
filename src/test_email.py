import smtplib
import json


from mailer import Mailer


jFilePath = "../infos/infos.json"
msg = "nigger"

mailer = Mailer(jFilePath)
print(mailer.load())
mailer.set_message(msg)
print(mailer.send())
