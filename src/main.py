from scrapper import WikiScrapper
from mailer import Mailer
from time_manager import TimeManager
from jobj import Jobj
import time
import re

		
if __name__ == "__main__":
	jFilePath = "../data/persons.json"
	error_log = "../logs/errors.log"
	credentials_path = "../infos/infos.json"

	tm = TimeManager(dm=1)

	mailer = Mailer(credentials_path)
	mailer.load()
	
	jObj = Jobj(jFilePath)

	prev_id = ""
	while True:
		time.sleep(0.1)
		if tm.execute():
			WikiScrapper.process(jObj, mailer, error_log)
			try:
				data, errors = mailer.check_mailbox(("sender", "id", "subject"))
				if len(errors):
					print(errors)
					continue
			except:
				print("Error reading mailbox.")
				continue

			if data["id"] != prev_id and "subject" in data:
				name = re.search(r"^(a|A)dd(.*?)$", data["subject"])
				if name is not None:
					res = jObj.add(name.group(2))
					args = (data["sender"], data["sender"], res, res)
				else:
					args = (data["sender"], data["sender"], "Something went wrong!", 
							f"Did send a correctly formatted mail?")
				mailer.send(*args)
				prev_id = data["id"]

			
