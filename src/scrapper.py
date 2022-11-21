import mechanicalsoup as msoup
import json
from os.path import exists
from mailer import Mailer

SIMPLE = 'infobox vcard'
PLAINLIST = 'infobox vcard plainlist'
BIOGRAPHY = 'infobox biography vcard'


""" Simple scrapper to get relevant info to alert about a person's death. """
class WikiScrapper:
	def __init__(self, jFilePath, credentials_path, error_log=""):
		try:
			self.jFilePath = jFilePath
			jFile = open(jFilePath, 'r')
			self.persons = json.load(jFile)
		except:
			print("JSON not correctly loaded. Check existence and conformity")
			return

		if exists(error_log):
			self.error_log = error_log
		else:
			self.error_log = "error_log.log"

		self.mailer = Mailer(credentials_path)
		self.browser = msoup.StatefulBrowser()
		self.freshly_dead = {}

	""" Launches directly the scrap. """
	@classmethod
	def process(cls, jFilePath, credentials_path, error_log=""):
		try:
			scrapper = cls(jFilePath, credentials_path, error_log)
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
				   for name, infos in self.persons.items()}
		# changes
		self.freshly_dead = [name for name, (is_dead, _) in results.items()
								if is_dead != self.persons[name]["dead"]]

		# update JSON
		# [self.persons[name].update({'dead':is_dead}) 
		# 	for name, (is_dead, _) in results.items()]

		with open(self.jFilePath, 'w+') as jFile:
			json.dump(self.persons, jFile, indent=6)

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
			mailto = ""
			subject = f"{name} has died!"
			body = f"! DEATHALERT INFO !\n{name} has died!"

			load_status.append(self.mailer.load())
			self.mailer.set_content(mailfrom, mailto, subject, body)
			send_status.append(self.mailer.send())
		return "error: load" not in load_status and "error: send" not in send_status
