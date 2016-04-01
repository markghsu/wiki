import webapp2
import json
import datetime
import time
import user
from models.pageModel import Page, Version
from google.appengine.api import memcache
from google.appengine.ext import db
from handlerparent import Handler
import logging

def getPage(name):
	page = memcache.get("page_"+name)
	logging.warning("trying to find")
	if not page:
		logging.warning("can't find "+name+" in memcache")
		query = Page.all().filter("name =",name).ancestor(wikiKey())
		page = query.get()
		logging.warning("query"+str(page));
		if page:
			memcache.set("page_"+name,page,100)
	return page

def getVersion(page,v):
	try:
		ver = int(v)
		query = Version.all().filter("version =",ver).ancestor(page)
		return query.get()
	except ValueError:
		return None

def savePage(p):
	logging.warning("saving"+str(p.name)+str(p.content)+str(p.parent)+str(p.version));
	p.put()
	#also saves a new version

	v = Version(parent=p, content=p.content, version=p.version)
	v.put()

	memcache.set("page_"+p.name,p,100)

# parent for all wiki posts.
def wikiKey(key="default"):
	logging.warning("wikikey: "+str(db.Key.from_path('wiki',key)))
	return db.Key.from_path('wiki',key)

class PageHandler(Handler):
	def get(self,name):
		p = getPage(name)
		if p:
			v = self.request.get('v')
			if v:
				version = getVersion(p,v)
				if version:
					self.render("page.html",title=name,content=version.content.replace('\n', '<br>'), loggedin=self.loggedin(), version=v)
				else:
					self.render("page.html",title=name,error="Error, version not found",content=p.content.replace('\n', '<br>'), loggedin=self.loggedin())
			else:
					self.render("page.html",title=name,content=p.content.replace('\n', '<br>'), loggedin=self.loggedin())
		else:
			self.redirect("/_edit/"+name)

class History(Handler):
	def get(self,name):
		p = getPage(name)
		if p:
			quer = Version.all().ancestor(p).order("-version")
			versions = quer.run()
			self.render("history.html",title=name,versions=versions, loggedin=self.loggedin())
		else:
			self.redirect("/_edit/"+name)


class EditPage(Handler):
	def get(self,name):
		if self.loggedin():	
			p = getPage(name)
			if p:
				v = self.request.get('v')
				if v:
					version = getVersion(p,v)
					if version:
						self.render("edit.html",title=name,content=version.content, loggedin=self.loggedin())
					else:
						self.render("edit.html",title=name,content=p.content, loggedin=self.loggedin())
				else:
					self.render("edit.html",title=name,content=p.content, loggedin=self.loggedin())
			else:
				self.render("edit.html",title=name, loggedin=self.loggedin())
		else:
			self.redirect("/login")
	def post(self,name):
		if self.loggedin():
			p = getPage(name)
			if p:
				p.content = self.request.get('content')
				p.name = name
				p.version += 1
			else:
				p = Page(parent=wikiKey(),name=name,content=self.request.get('content'), version = 1)
			savePage(p)
			self.redirect("/"+name)
		else:
			self.redirect("/login")			