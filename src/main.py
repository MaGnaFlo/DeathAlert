from scrapper import WikiScrapper
import os
import json

if __name__ == "__main__":
	jFilePath = "../data/persons.json"
	error_log = "../logs/errors.log"
	credentials_path = "../infos/infos.json"
	WikiScrapper.process(jFilePath, credentials_path, error_log)