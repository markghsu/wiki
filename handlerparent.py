import webapp2
import jinja2
import os
import hmac

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)

class Handler(webapp2.RequestHandler):
	SECRET = 'm2Snodfsgr34j3434gndfhewe34523y31xz'
	def user_hash(self,s):
		return hmac.new(Handler.SECRET,s).hexdigest()

	def make_user_hash(self,s):
		return "%s|%s" % (s, self.user_hash(s))

	def check_user_hash(self,h):
		val = h.split('|')[0]
		if h == self.make_user_hash(val):
			return val

	def loggedin(self):
		uid = self.request.cookies.get('user_id')
		return uid and self.check_user_hash(uid)

	def write(self,*a,**kw):
		self.response.out.write(*a,**kw)
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))