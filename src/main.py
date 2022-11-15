from scrapper import WikiScrapper
import os
import json

if __name__ == "__main__":
	jFilePath = "../data/persons.json"
	error_log = "../logs/errors.log"
	WikiScrapper.process(jFilePath, error_log)