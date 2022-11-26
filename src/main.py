from scrapper import WikiScrapper
from time_manager import TimeManager


if __name__ == "__main__":
	jFilePath = "../data/persons.json"
	error_log = "../logs/errors.log"
	credentials_path = "../infos/infos.json"

	tm = TimeManager(dm=10)

	while True:
		if tm.execute():
			WikiScrapper.process(jFilePath, credentials_path, error_log)