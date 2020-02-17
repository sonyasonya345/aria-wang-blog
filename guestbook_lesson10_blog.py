import os
import time
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.api import images

import jinja2

template_dir = os.path.join(os.path.dirname(__file__), "templates")
# set the jinjia2 environment and tell where it goes to look for template file
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class Handler(webapp2.RequestHandler):

  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))


class Art(db.Model):
  title = db.StringProperty(required=True)
  art = db.TextProperty(required=True)
  created = db.DateTimeProperty(auto_now_add=True)


class MainPage(Handler):

  def render_front(self, title="", art="", error=""):
    arts = db.GqlQuery("select * from Art order by created desc")
    self.render("front.html", title=title, art=art, error=error, arts=arts)

  def get(self):
    self.render_front()

  def post(self):
    title = self.request.get("title")
    art = self.request.get("art")

    if title and art:
      # create an instance of Art;
      # use object_art.put() method store the art object/instance into the database
      a = Art(title=title, art=art)
      a.put()

      # redirect to that specific art blog
      self.redirect("/")

    else:
      error = "We need both title and artwork!"
      self.render_front(title=title, art=art, error=error)


class FizzBuzz(Handler):

  def get(self):
    n = self.request.get("n")
    n = int(n)
    self.render("fizzbuzz.j2", n=n)


app = webapp2.WSGIApplication(
    [
        ("/", MainPage),
        ("/fizzbuzz", FizzBuzz),
    ],
    debug=True,
)
