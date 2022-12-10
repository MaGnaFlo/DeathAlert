import smtplib
import imaplib
import re
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

""" Simple mailing system """
class Mailer:
	def __init__(self, infoPath, verbose=True):
		self.verbose = verbose
		self.infoPath = infoPath
		self.sender = ""
		self.pwd = ""
		self.receiver = ""
		self.smtp = ""
		self.imap = ""
		self.port = -1
		self.message = ""

	""" Sets the info regarding the mail. """
	def load(self):
		try:
			jFile = open(self.infoPath, 'r')
			jObj = json.load(jFile)
			self.sender = jObj["user"]["address"]
			self.pwd = jObj["user"]["password"]
			self.smtp = jObj["server"]["smtp"]
			self.port = int(jObj["server"]["port"])
			self.imap = jObj["server"]["imap"]
			jFile.close()
			return "success"
		except:
			return "error: info"

	""" Format the mail to send. """
	def set_content(self, mailfrom="", mailto="", subject="", body=""):
		msg = MIMEMultipart()
		msg['From'] = mailfrom if mailfrom != "" else self.sender
		msg['To'] = mailto if mailto != "" else self.receiver
		msg['Subject'] = subject if subject != "" else "(None)"
		msg.attach(MIMEText(body, 'plain'))
		content = msg.as_string()
		self.content = content

	""" Sends the mail. """
	def send(self, sender, receiver, subject, body):
		self.set_content(sender, receiver, subject, body)

		session = smtplib.SMTP(self.smtp, self.port)
		session.starttls()

		if self.verbose:
			print('Login session...')
		try:
			session.login(self.sender, self.pwd)
		except:
			session.quit()
			return "Error: login"

		if self.verbose:
			print('Sending mail...')
		try:
			session.sendmail(self.sender, receiver, self.content)
		except:
			return "error: send"
		finally:
			session.quit()
			if self.verbose:
				print("Success!")
			return "success"

	def check_mailbox(self, data_keys) -> dict:
		def parse_mail(mail_text, keys) -> dict:
			data = {}
			errors = []
			if "body" in keys:
				try:
					exp_body = r'''Content-Type:text/html;charset="UTF-8"(.*?)--'''
					body = re.search(exp_body, mail_text).group(1)
					data.update({"body":body})
				except Exception as e:
					errors.append(("body", e))
			if "sender" in keys:
				try:
					exp_from = r"From:.*?<(.*?)>"
					sender = re.search(exp_from, mail_text).group(1)
					data.update({"sender":sender})
				except Exception as e:
					errors.append(("sender", e))
			if "subject" in keys:
				try:
					exp_subject = r"Subject:(.*?)(To|From)"
					subject = re.search(exp_subject, mail_text).group(1)
					data.update({"subject":subject})
				except Exception as e:
					errors.append(("subject", e))
			if "id" in keys:
				try:
					exp_id = r"Message-ID:<(.*?)>"
					message_id = re.search(exp_id, mail_text).group(1)
					data.update({"id":message_id})
				except Exception as e:
					errors.append(("id", e))
			return data, errors

		mail = imaplib.IMAP4_SSL(self.imap)
		mail.login(self.sender, self.pwd)
		mail.list()
		mail.select("inbox")

		result, data = mail.search(None, "ALL")
		ids = data[0]
		id_list = ids.split()
		latest_email_id = id_list[-1]
		result, data = mail.fetch(latest_email_id, "(RFC822)") # all mail data
		raw_email = data[0][1].decode("utf-8")
		mail_text = "".join(raw_email.split())

		if len(data_keys)==0:
			print("Warning: no keys provided for data retrieval.")
		data, errors = parse_mail(mail_text, data_keys)
		return data, errors
