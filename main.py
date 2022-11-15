from scrapper import WikiScrapper
import os
import json

jFilePath = "persons.json"

scrapper = WikiScrapper(jFilePath)
print(scrapper.check())
if scrapper.check():
	scrapper.process()