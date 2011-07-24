from google.appengine.api import users
import models
class YqlStrategy():
	result = None
	def __init__(self,result):
		self.result = result
	
	def process_results(self):
		pass

class BibliaOnlineStrategy(YqlStrategy):
	source = 'Biblia on-line'
	def process_results(self):
		content = self.result.rows['content']
		book = self.result.rows['a']['content']
		book = book.replace("\n"," ")
		source_link = self.result.rows['a']['href']
		title = book
		user = users.get_current_user()
		verse = models.Verse(
			content = content,
			book = book,
			source_link = source_link,
			title = title,
			user = user
		)
		verse.put()
		
		return verse

		

	
		
		
		