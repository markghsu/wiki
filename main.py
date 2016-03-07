import webapp2
import mainpage
import page
import user

app = webapp2.WSGIApplication([
    ('/', mainpage.MainPage),
    ('/signup/?', user.Signup),
    ('/login/?',user.Login),
    ('/logout/?',user.Logout),
    ('/([a-zA-Z0-9_-]+)/?', page.PageHandler),
    ('/_edit/([a-zA-Z0-9_-]+)/?', page.EditPage),
    ('/_history/([a-zA-Z0-9_-]+)/?', page.History)
], debug=True)
