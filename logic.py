from google.appengine.api import users
import models

BIBLIA_ONLINE = "bibliaonline"
FONTE_A_JORRAR = "fonteajorrar"


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

def process_results_fonte_a_jorrar(result):
	pass

process_strategy= {
	BIBLIA_ONLINE: process_results_biblia_online,
	FONTE_A_JORRAR: process_results_fonte_a_jorrar
}
	
		
		
		