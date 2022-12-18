import mechanicalsoup as msoup
import json
from os.path import exists
from mailer import Mailer

SIMPLE = 'infobox vcard'
PLAINLIST = 'infobox vcard plainlist'
BIOGRAPHY = 'infobox biography vcard'


""" Simple scrapper to get relevant info to alert about a person's death. """
class WikiScrapper:
	def __init__(self, jObj, mailer, error_log=""):
		self.jObj = jObj
		if exists(error_log):
			self.error_log = error_log
		else:
			self.error_log = "error_log.log"

		self.mailer = mailer
		self.browser = msoup.StatefulBrowser()
		self.freshly_dead = {}

	""" Launches directly the scrap. """
	@classmethod
	def process(cls, jObj, mailer, error_log=""):
		try:
			scrapper = cls(jObj, mailer, error_log)
			scrapper.areDead()
			success = scrapper.alert()
			if not success:
				raise Exception("Alerting procedure failed.")
		except:
			print("Processing failed.")
			return

	""" Checks if a person is dead via its Wikipedia page. """
	def isDead(self, browser, name):
		errors = ""
		url = f'https://en.wikipedia.org/wiki/{name}'
		try:
			browser.open(url)
		except:
			errors = f'Could not reach url {url} for {name}'
			return None, errors

		try:
			infobox = browser.page.find_all('table', attrs={'class':[SIMPLE, PLAINLIST, BIOGRAPHY]})
			infos = infobox[0].find_all('th', attrs={'scope':'row', 'class':'infobox-label'})
		except:
			errors= f'Could not find infobox for {url} for "{name}"'
			return None, errors

		is_dead = any(["died" in str(row).lower() for row in infos])
		return is_dead, errors

	""" Checks the death of a list of persons. """
	def areDead(self):
		results = {name:self.isDead(self.browser, infos['key']) 
				   for name, infos in self.jObj.persons.items()}
		# changes
		self.freshly_dead = [name for name, (is_dead, _) in results.items()
								if is_dead != self.jObj.persons[name]["dead"]
								and is_dead is not None]

		# update JSON
		[self.jObj.update(name, is_dead) for name, (is_dead, _) in results.items()]

		# write log
		with open(self.error_log, 'w') as log:
			[log.write("> "+res[1]+"\n") for res in results.values()
				if len(res[1])>0]

	""" Driiiing driiiing! """
	def alert(self):
		load_status = []
		send_status = []
		for name in self.freshly_dead:
			mailfrom = "DEATH ALERT"
			mailto = "melchior.myrrha@gmail.com"
			subject = f"{name} has died!"
			body = f"! DEATHALERT INFO !\n{name} has died!"
			send_status.append(self.mailer.send(mailfrom, mailto, subject, body))
		return "error: load" not in load_status and "error: send" not in send_status
		