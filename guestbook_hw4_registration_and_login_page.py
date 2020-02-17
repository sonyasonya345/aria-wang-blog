### Homewoke 4  / Lesson 13 ##########
"""
In homework4: 

- make a registration page: 
  1) username
  2) password: need to use hmac to hash the password
  3) verify password
  4) email
  - if user is already exsit, tell them to login and redirect to login page
  - if new users: store their info in the database

- make a log-in page:
  - check if user exist and
  - whether pasword correct: whether the password match with our hashed password

- make welcome page:
  - if successfully login or registered: welcome them by saying "Welcome, <username>!"

hash: 
- need to know how to hash password 
- need to know how to check whether somepasword is valid

database:
- need to know how to make database
- need to know what kind of database google webapp offer: video, images, string

cookie: 
- need to use cookie to check whether visit information is valid
- if not valid visit cookie info, means somebody might be hacking us
- if it is valid visit cookie info, then we can tell users how many times they have visited us.

"""
import os
import time
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.api import images

import jinja2
import hashlib
import hmac

import urllib2
from urllib2 import URLError

from xml.dom import minidom

# from jinja2 import Environment, PackageLoader, select_autoescape

template_dir = os.path.join(os.path.dirname(__file__), "templates")
# set the jinjia2 environment and tell where it goes to look for template file
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

# jinja_env = Environment(
#     loader=PackageLoader(template_dir),
#     autoescape=select_autoescape(['html', 'j2']),
# )


class Handler(webapp2.RequestHandler):

  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))


# secret = "secret"


def hash_str(s):
  """
  input: str
  output: str
  purpose: hash the string using hashlib md5
  """
  # return hashlib.md5(b"%s" % s).hexdigest()
  return hmac.new(b'secret', b"%s" % (s)).hexdigest()


def make_secure_val(s):
  """
  input s: str
  output hash_val: s
  """
  return "%s,%s" % (s, hash_str(s))


def check_secure_val(h):
  val = h.split(",")[0]
  if h == make_secure_val(val):
    return val


class User(db.Model):
  username = db.StringProperty(required=True)
  password = db.StringProperty(required=True)
  email = db.StringProperty()


class MainPage(Handler):

  def get(self):
    """
    purpose:
    1) get the visits info from cookie
    2) check whether the visits cookie is valid using check_secure_val()
    3) if valid, update it.
    """
    # set the response header type to text/plain
    self.response.headers['Content-Type'] = 'text/plain'
    visits = 0
    visits_cookie_str = self.request.cookies.get("visits")
    if visits_cookie_str:
      # print("make secure val", make_secure_val())
      cookie_val = check_secure_val(visits_cookie_str)
      if cookie_val:
        visits = int(cookie_val)
    visits += 1

    new_cookie_val = make_secure_val(str(visits))

    self.response.set_cookie("visits", value=new_cookie_val)

    if visits > 1000:
      self.write('you are the best ever!')
    else:
      self.write("You've been here %s times!" % str(visits))


class SignUp(Handler):

  def render_signup(self,
                    error="",
                    username="",
                    password="",
                    verify="",
                    email=""):
    self.render(
        "signup.html",
        error=error,
        username=username,
        password=password,
        verify=verify,
        email=email,
    )

  def get(self):
    self.render_signup()

  def post(self):
    username = self.request.get("username")
    password = self.request.get("password")
    verify = self.request.get("verify")
    email = self.request.get("email")
    print("username:{}, password:{}, verify:{}, email:{}".format(
        username,
        password,
        verify,
        email,
    ))

    if not verify_password(password, verify):
      error = "Your password does not match!"
      self.render_signup(error=error, username=username)

    new_user = check_new_user(username)

    if not new_user:
      error = "The user already exists!"
      self.render_signup(error=error, username=username)

    # # if user is new:
    elif new_user:
      u = User(username=username, password=password, email=email)
      u.put()

      # set cookie
      self.response.headers["Content-Type"] = 'text/plain'
      new_cookie_val = make_secure_val(username)
      self.response.set_cookie("user", value=new_cookie_val)
      self.redirect("/welcome")


def verify_password(password, verify):
  if (not password) or (not verify):
    return False
  if password == verify:
    return True
  return False


def check_new_user(username):
  users = db.GqlQuery("SELECT * FROM User")
  for user in users:
    print("user", user.username)
    if user.username == username:
      return False
  return True


class Welcome(Handler):

  def get(self):

    username_cookie_str = self.request.cookies.get("user")
    username = check_secure_val(username_cookie_str)
    self.render("welcome_sonya.html", username=username)


class LogIn(Handler):

  def render_login(self, error="", username=""):
    self.render("login_sonya.html", error=error, username=username)

  def get(self):
    self.render_login()

  def post(self):
    username = self.request.get("username")
    password = self.request.get("password")

    users = db.GqlQuery("SELECT * from User")
    for user in users:
      if user.username == username and user.password == password:
        # set cookie
        self.response.headers["Content-Type"] = "text/plain"
        user_cookie_val = make_secure_val(username)
        self.response.set_cookie("user", value=user_cookie_val)
        self.redirect("/welcome")

    error = "Sorry! Your username or password is incorrect!"
    self.render_login(error=error, username=username)


class LogOut(Handler):

  def get(self):
    self.response.delete_cookie("user")
    self.redirect("/login")


app = webapp2.WSGIApplication(
    [
        ("/", MainPage),
        ("/signup", SignUp),
        ("/welcome", Welcome),
        ("/login", LogIn),
        ("/logout", LogOut),
    ],
    debug=True,
)
