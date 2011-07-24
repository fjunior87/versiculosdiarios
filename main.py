#-*- encode: utf-8 -*-
import yql
import models
import wsgiref.handlers
import urllib, cgi
import logic

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template

old_xpath = 'select * from html where url="http://www.bibliaonline.com.br/" and xpath="/html/body/p[@class=\'ot verse\']"'
new_xpath = 'select * from html where url="http://www.bibliaonline.com.br/" and xpath="/html/body/p[@class=\'nt verse\']"'
def getRss():
	y = yql.Public()
	query = 'select * from html where url="http://www.bibliaonline.com.br/" and xpath="/html/body/p[@class=\'ot verse\']"'
	query
	result = y.execute(query)
	return result.rows['content']

class MainHandler(webapp.RequestHandler):
	def get(self):
		result = get_yql_result(old_xpath)
	
		self.response.out.write("Here")
		verseHandler = logic.YqlProcessor(result, logic.process_strategy[logic.BIBLIA_ONLINE])
		vars = verseHandler.process_results()
		
		self.response.out.write(vars.book)
		self.response.out.write(result.rows)
		
		result = get_yql_result(new_xpath)
		verseHandler.result = result
		vars = verseHandler.process_results()
		
		self.response.out.write(vars.book)
		self.response.out.write(result.rows)
		
		


def get_yql_result(query):
	y = yql.Public()
	result = y.execute(query)
	return result
		
class VerseHandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write(template.render("templates/add_verse.html",{}))
		
	def post(self):
		payload = dict(self.request.POST)
		
		verse = models.Verse(**payload)
		user = users.get_current_user()
		verse.user = user
		
		verse.put()
		
		self.response.out.write(verse.id)
		self.response.out.write(verse.created)
		self.response.out.write(verse.source)
		self.response.out.write(verse.sourceTitle)
		self.response.out.write(verse.content)
		self.response.out.write(verse.book)
		self.response.out.write(verse.title)
		self.response.out.write(verse.user)

#TODO:  Add A Verse Using YQL Content - BibiliaOnline
#TODO:  Add A Verse Using YQL Content - Caixa de Promessas
#TODO:  Login/Logout
#TODO:  Twitter Notification
#TODO:  A Good layouts
		
if __name__ == "__main__":
	application = webapp.WSGIApplication([
		('/', MainHandler),
		('/verse', VerseHandler),
		('/addVerse', VerseHandler),
		], debug=True)
	wsgiref.handlers.CGIHandler().run(application)