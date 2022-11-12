import mechanicalsoup as msoup

SIMPLE = 'infobox vcard'
PLAINLIST = 'infobox vcard plainlist'
BIOGRAPHY = 'infobox biography vcard'

names = ["Justin_Bieber", 
		 "Miles_Davis", 
		 "Avishai_Cohen_(bassist)",
		 "Steve_Vai",
		 "Keith_Richards",
		 "Vlad_the_Impaler",
		 "Marie_Curie",
		 "Vladimir_Putin"]

def check_if_dead(browser, name):
	errors = []
	url = f'https://en.wikipedia.org/wiki/{name}'
	try:
		browser.open(url)
	except:
		errors.append(f'Could not reach url {url} for {name}')
		return None, errors

	try:
		infobox = browser.page.find_all('table', attrs={'class':[SIMPLE, PLAINLIST, BIOGRAPHY]})
		infos = infobox[0].find_all('th', attrs={'scope':'row', 'class':'infobox-label'})
	except:
		errors.append(f'Could not find infobox for {url} for {name}')
		return None, errors

	is_dead = any(["died" in str(row).lower() for row in infos])
	return is_dead, errors

def check_name_list(browser, name_list):
	results = {name:check_if_dead(browser, name) for name in name_list}
	errors = [res[1] for res in results.values()]
	results = {name: res[0] for name, res in results.items()}
	return results, errors

browser = msoup.StatefulBrowser()
results, errors = check_name_list(browser, names)
print(results)
print(errors)
