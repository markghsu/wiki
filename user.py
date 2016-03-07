import webapp2
import json
import datetime
import time
from models.userModel import User
from google.appengine.api import memcache
from google.appengine.ext import db
from handlerparent import Handler
import logging
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def error_username(username):
	q = User.by_name(username)
	if not USER_RE.match(username):
		return "That's not a valid username."
	elif q:
		return "That username is taken."
	else:
		return ""

PASS_RE = re.compile(r"^.{3,20}$")
def error_password(st):
	if not PASS_RE.match(st):
		return "That wasn't a valid password."
	else:
		return ""


EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def error_email(st):
	if st:
		if not EMAIL_RE.match(st):
			return "That's not a valid email."
		else:
			return ""
	else:
		return ""

class Signup(Handler):
	def get(self):
		self.render("signup.html")
	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')
		ue = error_username(username)
		pe = error_password(password)
		ve = "Your passwords didn't match." if password!=verify else ""
		ee = error_email(email)

		if not (ue or pe or ve or ee):
			userhash = self.make_user_hash(username)
			muser = User.register(name=username,pw=password,email=email)
			
			muser.put()
			
			#add to DB and set login cookie
			self.response.headers.add_header('Set-Cookie', str('user_id=%s; Path=/'% userhash))
			self.redirect("/")
		else:
			self.render("signup.html",username=username,uerror=ue,perror=pe,verror=ve,email=email,eerror=ee)

class Login(Handler):
	def get(self):
		self.render("login.html")
	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		u = User.login(name=username,pw=password)
		if u:
			#set logged in cookie
			userhash = self.make_user_hash(username)
			self.response.headers.add_header('Set-Cookie', str('user_id=%s; Path=/'% userhash))
			self.redirect("/")
		else:
			self.render("login.html",username=username, error="Incorrect username/password, please try again.")

class Logout(Handler):
	def get(self):
		#remove cookie, reload login page
		self.response.headers.add_header('Set-Cookie', str('user_id=; Path=/'))
		self.redirect("/login")