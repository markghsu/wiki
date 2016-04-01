import webapp2
import json
import datetime
import time
from google.appengine.api import memcache

from handlerparent import Handler
from google.appengine.ext import db

class MainPage(Handler):
	def get(self):
		#gp = getPosts()
		self.render("front.html",title="",time='%.4f'%(time.time()),loggedin=self.loggedin())