#-*- encode: utf-8 -*-
from google.appengine.api import users
import models

BIBLIA_ONLINE = "bibliaonline"
FONTE_A_JORRAR = "fonteajorrar"
ARCA_UNIVERSAL = "arcauniversal"

class YqlProcessor():
	result = None
	process = None
	def __init__(self,result,process):
		self.result = result
		self.process = process
	
	def process_results(self):
		return self.process(self.result)

	
def process_results_biblia_online(result):
	source = 'Biblia on-line'
	if result.rows:
		content = result.rows['content']
		book = result.rows['a']['content']
		book = book.replace("\n"," ")
		source_link = result.rows['a']['href']
		title = book
		user = users.get_current_user()
		verse = models.Verse(
			content = content,
			book = book,
			sourceLink = source_link,
			title = title,
			user = user,
			source = source
		)
		verse.put()
		
		return verse

def process_results_arca_universal(result):
	import urllib
	import re
	source = "Arca Universal"
	source_link = "http://www.arcauniversal.com/servicos/caixadepromessas.html"
				
	versePattern = "<h4>(.*)</h4>"
	bookPattern = "<span class=\"style1\">(.*)</span>"
	
	if result.content:
		requestContent = result.content
		verseRegex = re.search(versePattern,requestContent)
		bookRegex = re.search(bookPattern,requestContent)
		if verseRegex and bookRegex:
		
			verseContent = verseRegex.group(1).decode("utf8")
			book = bookRegex.group(1).replace(".",":").decode("utf8")
			title = book
			
			verse = models.Verse(
				content = verseContent,
				book = book,
				sourceLink = source_link,
				title = title,
				user = users.get_current_user(),
				source = source
			)
			verse.put()
			
			return verse
	
	

process_strategy= {
	BIBLIA_ONLINE: process_results_biblia_online,
	ARCA_UNIVERSAL: process_results_arca_universal
}
	
		
		
		