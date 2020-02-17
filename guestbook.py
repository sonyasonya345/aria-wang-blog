# #!/usr/bin/env python

# # Copyright 2016 Google Inc.
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #     http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.

# # [START imports]
# import os
# import urllib
# import cgi

# from google.appengine.api import users
# from google.appengine.ext import ndb

# import jinja2
# import webapp2

# JINJA_ENVIRONMENT = jinja2.Environment(
#     loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
#     extensions=['jinja2.ext.autoescape'],
#     autoescape=True)
# # [END imports]
# """
# Addition Options for Aria's main page.

#     <input type="radio" name="activity" value="Aria Dance with Rap Music"> Aria Dancing with Rap Music <br>
#     <input type="radio" name="activity" value="Aria Eating Furiously"> Aria Eating Furiously <br>
#     <input type="radio" name="activity" value="Aria's Shy Moment"> Aria's Shy Moment <br>

# """

# welcome = """
# <!DOCTYPE html>
# <html>
# <body>

# <h2 title="I'm a header"> Welcome to <strong>Aria's World!</strong></h2>

# <p title="introduction">
# I am <strong>cute cute Aria</strong>. Welcome to my space. You can choose one of my below happy moments and enjoy it! >_<
# </p>

# <div>
# <form action = "/activityform">

#     <label>Aria
#         Dancing with Rap Music
#         <input type="radio" name="activity" value="Aira Dance with Rap Music">
#     </lable>
#     <br>

#     <label>
#         Aria Eating Furiously
#     <input type="radio" name="activity" value="Aria Eating Furiously">
#     </lable>
#     <br>

#     <label>Aria's Shy Moment
#     <input type="radio" name="activity" value="Aria's Shy Moment">
#     </label>
#     <br>

#     <input type="submit">

# </form>
# </div>

# <img src="images/aria_front_page.jpg" alt="My Cutie Moment">

# </html>
# <br>
# <br>
# <br>
#  """

# birthday_form = """
# <!DOCTYPE html>
# <html>

# <div style="color: red">%(error)s</div>

# <h2>
#   Let's Play a Game!!!
# </h2>

# <p title="introduction">
#   Do you know my <strong>Birthday</strong> ?
# </p>

# <form method="post">

#   <label>
#     Month
#     <input type="text" name="month" value="%(month)s">
#   </label>

#   <label>
#     Day
#     <input type="text" name="day" value="%(day)s">
#   </label>

#   <label>
#     Year
#     <input type="text" name="year" year="%(year)s">
#   </label>

#   <br>
#   <br>
#   <input type="submit">
#  """

# ######################## Class Form ########################

# form = """
# <form method="post">
#     What is your birthday?
#     <br>

#     <label>
#       Month
#       <input type="text" name="month" value="%(month)s">
#     </lable>

#     <label>
#       Day
#       <input type="text" name="day" value="%(day)s">
#     </label>

#     <label>
#       Year
#       <input type="text" name="year" value="%(year)s">
#     </label>

#     <div style="color:red">%(error)s</div>

#     <br>
#     <br>
#     <input type="submit">
# </form>
# """

# # form = """
# # <form method="post" action="/form">
# #     <input name="q" />
# #     <input type="submit" />
# # </form>
# # """

# # [START main_page]

# button = "aria"

# # button = "class"

# class MainPage(webapp2.RequestHandler):

#   def __init__(self, *args, **kwargs):
#     super(MainPage, self).__init__(*args, **kwargs)
#     #   self.button = "aria"
#     #   # self.button = "class"
#     global button
#     self.button = button

#   def write_form(self, month="", day="", year="", error=""):
#     # if self.button == "aria":
#     if self.button == "aria":
#       self.response.out.write(
#           birthday_form % {
#               "month": self.escape_html(month),
#               "day": self.escape_html(day),
#               "year": self.escape_html(year),
#               "error": self.escape_html(error),
#           })
#     elif self.button == "class":
#       self.response.out.write(
#           form % {
#               "month": self.escape_html(month),
#               "day": self.escape_html(day),
#               "year": self.escape_html(year),
#               "error": self.escape_html(error),
#           })

#   def escape_html(self, string):
#     return cgi.escape(string, quote=True)

#   def get(self):
#     if self.button == "aria":
#       self.response.out.write(welcome)
#       # self.response.out.write(birthday_form)
#       self.write_form()

#     ####################### class #######

#     elif self.button == "class":
#       # self.response.headers['Content-Type'] = ''
#       # self.response.out.write(form)
#       self.write_form()

#   def post(self):
#     months = [
#         "January",
#         "February",
#         "March",
#         "April",
#         "May",
#         "June",
#         "July",
#         "August",
#         "September",
#         "October",
#         "November",
#         "December",
#     ]

#     months_dict = dict((m[:3].lower(), m) for m in months)

#     def valid_month(month):
#       key = month[:3].lower()
#       if key in months_dict:
#         return months_dict[key]
#       return None

#     def valid_day(day):
#       """
#       input day: str
#       return int
#       """
#       if day.isdigit():
#         day = int(day)
#         if day > 0 and day <= 31:
#           return day
#       return

#     def valid_year(year):
#       """
#       input year: str
#       return intz
#       """
#       if year.isdigit():
#         year = int(year)
#         if year >= 1900 and year <= 2020:
#           return year
#       return

#     user_month = valid_month(self.request.get("month"))
#     user_day = valid_day(self.request.get("day"))
#     user_year = valid_year(self.request.get("year"))

#     month = self.request.get("month")
#     day = self.request.get("day")
#     year = self.request.get("year")

#     ################### aria post part ###########

#     if self.button == "aria":
#       if (user_month == "December" and user_day == 1 and user_year == 2017):
#         self.redirect("/thanks")
#       else:
#         self.write_form(
#             month=month,
#             day=day,
#             year=year,
#             error=
#             "You did not get it correct. <br> Do you want to guess it again?")

#     ################ class post part ##############
#     elif self.button == "class":

#       if (user_month and user_day and user_year):
#         self.redirect("/thanks")
#       else:
#         # self.response.out.write("not valid day.")
#         # self.response.out.write(form)
#         self.write_form(
#             month=month,
#             day=day,
#             year=year,
#             error="You did not get this correct! let's enter valid date!")

# ####################### Thanks Handler Share  ###########################################

# class ThanksHandler(webapp2.RequestHandler):
#   """
#   i am inheriting the property of webapp2.RequestHandler,
#   so I still need tu super function to make it works
#       self.write_form()

#   """

#   def __init__(self, *args, **kwargs):
#     super(ThanksHandler, self).__init__(*args, **kwargs)
#     global button
#     self.button = button

#   def get(self):
#     if self.button == "aria":
#       self.response.out.write(
#           "Yeah! You got it correct!!!! <br> My Birthday is December 1st, 2017!!!!"
#       )
#     elif self.button == "class":
#       self.response.out.write("<html>Yeah, you got a valid day! <br></html>")

# class TestHandler(webapp2.RequestHandler):

#   def post(self):
#     # q = self.request.get("q")
#     # self.response.out.write(q)

#     self.response.headers['Content-Type'] = 'text/plain'
#     self.response.out.write(self.request)

# ################ Aria Veriosn ######################
# class ActivityHandler(webapp2.RequestHandler):

#   def get(self):
#     # aria version
#     q = self.request.get("activity")
#     self.response.out.write(q)

# #########################################################################

# app = webapp2.WSGIApplication(
#     [
#         ('/', MainPage),  # share
#         ('/activityform', ActivityHandler),  # aria
#         ('/form', TestHandler),  # class
#         ('/thanks', ThanksHandler)  # share
#     ],
#     debug=True)
# # [END app]

# ############################################################################################
# ############################################################################################
# ############################################################################################
# ############################################################################################
# ############################################################################################
# ###################################  Lesson 15 class 20-21 #####################################################
"""
Task:

- create a Aria page
- where users can create new Aria blog: title and content.

- Front page:
  1) Should show please create a new blog
  2) Most recent 10 blogs

- When new blog is created by users, redirect them to a permalink.
"""

import os
import time
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import memcache
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

import jinja2

import urllib2
from urllib2 import URLError

import xml.dom.minidom
import bs4
from bs4 import BeautifulSoup
import requests

import logging
import time

template_dir = os.path.join(os.path.dirname(__file__), "templates")
# set the jinjia2 environment and tell where it goes to look for template file
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


def get_blog_url(blog):
  return '/aria/%s' % blog.key.id()


class Handler(webapp2.RequestHandler):

  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))


class Handler2(blobstore_handlers.BlobstoreUploadHandler):

  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))


class Handler3(blobstore_handlers.BlobstoreDownloadHandler):

  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))


class Blog(ndb.Model):
  title = ndb.StringProperty(required=True)
  article = ndb.TextProperty(required=True)
  photo_key = ndb.BlobKeyProperty()
  photo_url = ndb.StringProperty()
  created = ndb.DateTimeProperty(auto_now_add=True)


class FrontPage(Handler):

  def get(self):
    blogs = ndb.gql("select * from Blog order by created desc limit 10")
    upload_url = blobstore.create_upload_url('/upload_photo')
    self.render(
        "aria_frontpage.html",
        blogs=blogs,
        upload_url=upload_url,
        get_blog_url=get_blog_url)


class PhotoUploadHandler(Handler2):
  """
  - Then the Blobstore creates a blob from the uploaded content.
  - this blob has a blob key which you can use to refernce or retrieve it later
  - then you can save this blob as an UserPhoto entity, and set its blob_key
  """

  def _make_blog(self):
    title = self.request.get('title')
    article = self.request.get('article')
    blog_args = {
        'title': title,
        'article': article,
    }
    uploads = self.get_uploads()
    if uploads:
      photo = uploads[0]
      photo_key = photo.key()
      photo_url = images.get_serving_url(photo_key)
      blog_args.update({
          'photo_key': photo_key,
          'photo_url': photo_url,
      })

    return Blog(**blog_args)

  def post(self):
    title = self.request.get("title")
    article = self.request.get("article")

    if not title or not article:
      error = "Please complete the required field"
      self.render(
          "aria_frontpage.html",
          title=title,
          article=article,
          error=error,
      )

    blog = self._make_blog()
    blog_key = blog.put()
    self.redirect("/aria/%s" % (blog_key.id()))


class BlogPage(Handler):

  def get(self, blog_id):
    """
    purpose: to render the relavant blogs
    # retrieve the entity from db
    # https://cloud.google.com/appengine/docs/standard/python/datastore/entities#Python%202_Retrieving_an_entity
    # github example: https://github.com/minfawang/sonya/blob/master/image_example/guestbook.py
    """
    print("my blog id is", blog_id, ". \nThe type is", type(blog_id))
    blog = ndb.Key("Blog", long(blog_id)).get()
    # blog.photo_url = images.get_serving_url(blog.photo_key)
    self.render("aria_blogpage.html", blog=blog)


app = webapp2.WSGIApplication(
    [
        ("/", FrontPage),
        ('/upload_photo', PhotoUploadHandler),
        ("/aria/([0-9]+)", BlogPage),
    ],
    debug=True,
)
