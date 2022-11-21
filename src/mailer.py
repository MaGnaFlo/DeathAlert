import smtplib
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
		self.server = ""
		self.port = -1
		self.message = ""

	""" Sets the info regarding the mail. """
	def load(self):
		try:
			jFile = open(self.infoPath, 'r')
			jObj = json.load(jFile)
			self.sender = jObj["user"]["address"]
			self.pwd = jObj["user"]["password"]
			self.receiver = jObj["receiver"]["address"]
			self.server = jObj["SMTP"]["server"]
			self.port = int(jObj["SMTP"]["port"])
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
		text = msg.as_string()
		self.content = text

	""" Sends the mail. """
	def send(self):
		session = smtplib.SMTP(self.server, self.port)
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
			session.sendmail(self.sender, self.receiver, self.content)
		except:
			return "error: send"
		finally:
			session.quit()
			return "success"
