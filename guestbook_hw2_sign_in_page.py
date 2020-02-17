#!/usr/bin/env python

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

import cgi
import string

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

form = """
<!DOCTYPE html>
<html>
  <h1> Sign In Page </h1>

  <h2 style="color:red;">%(error)s</h2>

  <body>


  <br>
  <br>

  <form method="post">
    <lable>
      User Name
      <input type="text" name="username" value="%(username)s">
    </label>

    <br>
    <br>

    <lable>
      Password
      <input type="password" name="password" value="%(password)s">
    </lable>

    <br>
    <br>

    <label>
      Verfiy Password
      <input type="password" name="verifypassword" value="%(verifypassword)s">
    </label>

    <br>
    <br>

    <label>
      Email (Optional)
      <input type="text" name="email" value="%(email)s">
    </label>

    <br>
    <br>
    <input type="submit">
  </form>

  </body>

</html>
"""


class MainPage(webapp2.RequestHandler):

  def escape_html(self, string):
    return cgi.escape(string, quote=True)

  def write_form(self,
                 error="",
                 username="",
                 password="",
                 verifypassword="",
                 email=""):
    self.response.out.write(
        form % {
            "error": error,
            "username": username,
            "password": password,
            "verifypassword": verifypassword,
            "email": email,
        })

  def check_password(self, password, verifypassword):
    if password == verifypassword:
      return True
    return False

  def check_username(self, username):
    return (" " not in username)

  def get(self):
    self.write_form()

  def post(self):
    username = self.request.get("username")
    password = self.request.get("password")
    verifypassword = self.request.get("verifypassword")
    email = self.request.get("email")

    username_ok = self.check_username(username)
    password_ok = self.check_password(password, verifypassword)

    if username_ok and password_ok:
      self.response.out.write("Welcome! %s" % username)
    else:
      if not username_ok:
        self.write_form(
            error="Your username is invalid Please enter again!", email=email)
      elif not password_ok:
        self.write_form(
            error="Your password does NOT match! Please enter again",
            username=username,
            email=email)


app = webapp2.WSGIApplication([('/', MainPage)])
