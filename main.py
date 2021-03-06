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
from google.appengine.ext import db

old_xpath = 'select * from html where url="http://www.bibliaonline.com.br/" and xpath="//p[@class=\'ot verse\']"'
new_xpath = 'select * from html where url="http://www.bibliaonline.com.br/" and xpath="//p[@class=\'nt verse\']"'
def getRss():
	y = yql.Public()
	query = 'select * from html where url="http://www.bibliaonline.com.br/" and xpath="/html/body/p[@class=\'ot verse\']"'
	query
	result = y.execute(query)
	return result.rows['content']

class MainHandler(webapp.RequestHandler):
	def get(self):
		if self.request.headers.get("X-AppEngine-Cron","") == "true":
	
			result = get_yql_result(old_xpath)
			
			verseHandler = logic.YqlProcessor(result, logic.process_strategy[logic.BIBLIA_ONLINE])
			verseHandler.process_results()
			
			result = get_yql_result(new_xpath)
			
			verseHandler.result = result
			verseHandler.process_results()
			
			logic.YqlProcessor(get_arca_universal_result(), logic.process_strategy[logic.ARCA_UNIVERSAL]).process_results()
			
			self.response.out.write("Verses Added")


def get_yql_result(query):
	y = yql.Public()
	result = y.execute(query)
	return result
	
def get_arca_universal_result():
	form_fields = {
		"idp": "131",
	}
	form_data = urllib.urlencode(form_fields)
	result = urlfetch.fetch(url="http://www.arcauniversal.com/servicos/pg_caixa_promessa_random.html",
							payload=form_data,
							method=urlfetch.POST,
							headers={'Content-Type': 'application/x-www-form-urlencoded'})
	return result
		
class VerseHandler(webapp.RequestHandler):
	def get(self):
		if self.request.path == '/':
			verses = db.GqlQuery('SELECT * FROM  Verse ORDER by created DESC')
			self.response.out.write(template.render("templates/verses_index.html",{"verses":verses}))
		else:
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
		('/cron', MainHandler),
		('/verse', VerseHandler),
		('/addVerse', VerseHandler),
		('/',VerseHandler),
		], debug=True)
	wsgiref.handlers.CGIHandler().run(application)