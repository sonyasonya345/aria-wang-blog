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
<body>

<h2 title="I'm a header"> Enter some text into ROT13</strong></h2>

<form method="post">
  <textarea name="textarea" style="width:250px;height:150px;">%(textarea)s</textarea>

  <br>
  <input type="submit">
</form>
"""


class MainPage(webapp2.RequestHandler):

  def get(self):
    # self.response.out.write(form)
    self.write_form()

  def write_form(self, textarea=""):
    return self.response.out.write(
        form % {"textarea": self.escape_html(textarea)})

  def escape_html(self, string):
    return cgi.escape(string, quote=True)

  def process(self, s):
    """
    ab!c
    ab!c
    ab&!c
    """
    result = ""
    for w in s:
      if w == " ":
        result += w
      elif w in string.digits:
        result += w
      elif w == ('&' or '<' or '>' or '"'):
        # w1 = self.escape_html(w)
        # result += w1
        result += w
      elif w in string.punctuation:
        result += w
      elif w in string.ascii_lowercase:
        i = string.ascii_lowercase.index(w)
        i += 13
        i %= 26
        result += string.ascii_lowercase[i]
      elif w in string.ascii_uppercase:
        i = string.ascii_uppercase.index(w)
        i += 13
        i %= 26
        result += string.ascii_uppercase[i]
    return result

  def post(self):
    content = self.request.get("textarea")
    new_content = self.process(content)
    print("new_content", new_content)
    # self.response.out.write(new_content)
    self.write_form(textarea=new_content)


app = webapp2.WSGIApplication([
    ('/', MainPage),
])
