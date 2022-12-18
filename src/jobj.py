import json

""" Class treating the json file containing the persons infos."""
class Jobj:
	def __init__(self, jFilePath):
		try:
			self.jFilePath = jFilePath
			jFile = open(jFilePath, 'r')
			self.persons = json.load(jFile)
			jFile.close()
		except:
			print("JSON not correctly loaded. Check existence and conformity")

	def add(self, name):
		""" Adds a name to the file."""
		if name in list(self.persons.keys()):
			return "Name already in the list."

		key = "_".join(name.split(" "))
		json_dict = {"key" : key, "dead" : False}
		self.persons[name] = json_dict
		self.save()
		return f"{name} successfully added to the list!"

	def update(self, name, is_dead):
		""" Updates the file accordiing to a dictionary."""
		self.persons[name]["dead"] = is_dead
		self.save()

	def save(self):
		""" Write modification."""
		try:
			jFile = open(self.jFilePath, 'w+')
			json.dump(self.persons, jFile, indent=6)
			jFile.close()
		except:
			print("nope")