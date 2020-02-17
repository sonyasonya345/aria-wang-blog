############ version 1 baby version of shopping list ############

import os
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2

template_dir = os.path.join(os.path.dirname(__file__), "templates")
# set the jinjia2 environment and tell where it goes to look for template file
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

form_html = """
<!DOCTYPE html>
<html>
  <h2> Shopping Cart </h2>
    <form>
      <input type="text" name="food">
      %s
      <br>
      <button type="button">add</button>
      <button type="submit">addfaake</button>
      <input type="submit">
    </form>

"""

hidden_html = """
  <input type="hidden" name="food" value="%s">
"""

item_html = """
<li>%s</li>
"""

shopping_list_html = """
<br>
<br>

<h2> Shopping List </h2>
  <ul>
    %s
  </ul>
"""


class Handler(webapp2.RequestHandler):

  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinjia_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))


class MainPage(Handler):

  def get(self):
    hidden_output = ""
    items_list = ""

    items = self.request.get_all("food")
    if items:
      for item in items:
        hidden_output += (hidden_html % item)
        items_list += (item_html % item)

    shopping_list = shopping_list_html % items_list
    form = form_html % hidden_output

    output = form + shopping_list
    # print("output", output)
    self.write(output)


app = webapp2.WSGIApplication(
    [
        ("/", MainPage),
    ],
    debug=True,
)

############################################################################################
############################################################################################
#################### Jinjia version of Shopping List  ######################################

import os
import time
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import db

import jinja2

form_html = """
<!DOCTYPE html>
<html>
  <h2> Shopping Cart </h2>
    <form>
      <input type="text" name="food">
      %s
      <br>
      <button type="button">add</button>
    </form>

"""

hidden_html = """
  <input type="hidden" name="food" value="%s">
"""

item_html = """
<li>%s</li>
"""

shopping_list_html = """
<br>
<br>

<h2> Shopping List </h2>
  <ul>
    %s
  </ul>
"""

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
    print('render_front()')
    arts = db.GqlQuery("select * from Art order by created desc")
    self.render("front.html", title=title, art=art, error=error, arts=arts)

  def get(self):
    # items = self.request.get_all("food")
    # self.render("shopping_list.j2", items=items)
    self.render_front()

  def post(self):
    title = self.request.get("title")
    art = self.request.get("art")

    if title and art:
      # create an instance of Art;
      # use object_art.put() method store the art object/instance into the database
      a = Art(title=title, art=art)
      a.put()

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
