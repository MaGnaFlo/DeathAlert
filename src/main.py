from scrapper import WikiScrapper
from mailer import Mailer
from time_manager import TimeManager
import time


if __name__ == "__main__":
	jFilePath = "../data/persons.json"
	error_log = "../logs/errors.log"
	credentials_path = "../infos/infos.json"

	tm = TimeManager(dm=1)

	mailer = Mailer(credentials_path)
	mailer.load()
	

	# scrapper = WikiScrapper(jFilePath, mailer, error_log)

	prev_id = ""
	while True:
		time.sleep(0.1)
		if tm.execute():
			data, errors = mailer.check_mailbox(("sender", "id"))
			if len(errors):
				print(errors)
				continue
			if data["id"] != prev_id:
				args = (data["sender"], data["sender"], "received!", "hello friend.")
				mailer.send(*args)
				prev_id = data["id"]
	# 		WikiScrapper.process(jFilePath, credentials_path, error_log)
