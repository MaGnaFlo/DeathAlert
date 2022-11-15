import mechanicalsoup as msoup
from os.path import exists
import json

SIMPLE = 'infobox vcard'
PLAINLIST = 'infobox vcard plainlist'
BIOGRAPHY = 'infobox biography vcard'

class WikiScrapper:
	def __init__(self, jFilePath, error_log=""):
		try:
			jFile = open(jFilePath)
			self.persons = json.load(jFile)
			self.correctly_loaded = True
		except:
			self.correctly_loaded = False
			print("JSON not correctly loaded. Check existence and conformity")
			return

		if exists(error_log):
			self.error_log = error_log
		else:
			self.error_log = "error_log.log"

		self.browser = msoup.StatefulBrowser()

	def check(self):
		return self.correctly_loaded

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

	def process(self):
		results = {name:self.isDead(self.browser, infos['key']) 
				   for name, infos in self.persons.items()}

		# update JSON
		[self.persons[name].update({'dead':is_dead}) 
			for name, is_dead in results.items()]

		# write log
		with open(self.error_log, 'w') as log:
			[log.write("> "+res[1]+"\n") for res in results.values()
				if len(res[1])>0]