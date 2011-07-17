import time
from google.appengine.ext import db

#Took from the scriptlets project
#http://github.com//scriptlets
def baseN(num,b=62,numerals="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"): 
    return ((num == 0) and  "0" ) or (baseN(num // b, b).lstrip("0") + numerals[num % b])

class Verse(db.Model):
	user = db.UserProperty(auto_current_user_add=True)
	content = db.TextProperty()
	created = db.DateTimeProperty(auto_now_add=True)
	source = db.StringProperty()
	sourceLink = db.StringProperty()
	sourceTitle = db.StringProperty()
	book = db.StringProperty()
	id = db.StringProperty(required=True)
	title = db.StringProperty(required=True)
	
	def __init__(self, *args, **kwargs):
		kwargs['id'] = kwargs.get('id', baseN(abs(hash(time.time()))))
		super(Verse, self).__init__(*args, **kwargs)