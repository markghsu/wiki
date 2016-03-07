import webapp2
import json

from google.appengine.ext import db

class Page(db.Model):
	name = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	version = db.IntegerProperty(required=True)

class Version(db.Model):
	content = db.TextProperty(required = True)
	version = db.IntegerProperty(required=True)
	created = db.DateTimeProperty(auto_now_add = True)