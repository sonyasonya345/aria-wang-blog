"""
Task:

- create a website that people can submit arts

- create a map on the mainpage showing the geo coordinates of the recent 10 users.
- use memchaced to reduce the reading from database

"""

import os
import time
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import memcache

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


class Handler(webapp2.RequestHandler):

  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))

  def gmaps_img(self, points):
    GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"
    markers = "&".join(
        ["markers={},{}".format(point.lat, point.lon) for point in points])
    GMAPS_URL += markers
    return GMAPS_URL


#### class version of getting coordinates
# def get_coords(ip):
#   """
#   purpose: using the ip address of the user to get their geo coordinates

#   input ip: string
#   output (lat, lon): unicode
#   """
#   ip_url = "http://api.hostip.info/?ip="
#   url = ip_url + ip
#   content = None
#   try:
#     content = urllib2.urlopen(url).read()
#     # print("yes")
#   except URLError:
#     print("error")
#     return

#   if content:
#     doc = minidom.parseString(content)

#     geo_node = doc.getElementsByTagName("gml:coordinates")[0]
#     if geo_node and geo_node.firstChild.data:
#       lon, lat = geo_node.firstChild.data.split(",")
#       return db.GeoPt(lat, lon)


def get_coords(ip):
  url = "https://www.melissa.com/v2/lookups/iplocation/ip?ip={}".format(ip)

  response = urllib2.urlopen(url)
  html = response.read()  # html is a html string

  soup = BeautifulSoup(html, "html.parser")
  print("soup", soup)

  coords = soup.tbody.find_all('td')[13].string

  lat, lon = coords.split(" ")
  return db.GeoPt(lat, lon)


class Art(db.Model):
  title = db.StringProperty(required=True)
  art = db.TextProperty(required=True)
  created = db.DateTimeProperty(auto_now_add=True)
  coords = db.GeoPtProperty()


def top_arts(update=False):
  """
  purpose 1: sql the most recent arts and store it. 
  - if there is new piece of arts submitted, we do sql request to call for most recent arts.
  - if the users is not submitting any new art, we can just use the latest arts we store in arts_cache dictionary.

  purpose 2:
  - check how much time in seconds has passed from latest databased query since the websute has been initiated / launched.
  """
  key = "top"
  arts = memcache.get(key)
  time_passed = memcache.get("time_passed")

  if time_passed is None:
    start_time = time.time()
    memcache.set("start_time", start_time)

  if arts is None or update:
    logging.error("DB QUERY")  # pri nt string " db query" k

    arts = db.GqlQuery("select * from Art order by created desc")
    # create a list from the iterable, so we don't have to call googel query every time
    arts = list(arts)
    memcache.set(key, arts)
    current_time = time.time()

    # update time_passed
    start_time = memcache.get("start_time")
    time_passed = current_time - start_time
    memcache.set("time_passed", time_passed)

  return arts, time_passed


class MainPage(Handler):

  def render_front(self, title="", art="", error=""):
    """
    - render the most recent arts by calling the top_arts() function
    """
    arts, time_passed = top_arts()
    # print("arts", arts.items())
    """
    - need to find if any arts has coordinates
    - if any arts has any coords, display the google map with the right coordinates on it.
    - display the image url
    """
    # points = filter(None, [art_inner.coords for art_inner in arts])
    # # self.write(repr(points))

    # img_url = None
    # if points:
    #   img_url = self.gmaps_img(points)

    self.render(
        "front.html",
        title=title,
        arts=arts,
        error=error,
        art=art,
        # img_url=img_url,
        time_passed=time_passed,
    )

  def get(self):
    self.render_front()
    # memcache.flush_all()
    # print("check arts_cache", arts_cache.items())

  def post(self):
    title = self.request.get("title")
    art = self.request.get("art")

    if title and art:
      # create an instance of Art;
      # use object_art.put() method store the art object/instance into the database
      a = Art(title=title, art=art)
      ## comment the coordiantes requests for now
      # ip = "4.2.2.2"
      # coords = get_coords(ip)
      # if coords:
      #   a.coords = coords

      a.put()  # put arts in the database
      time.sleep(0.5)

      top_arts(update=True)
      """
      My version of updating cache
      """
      # # update the arts_cache
      # key = "top"
      # if key not in arts_cache:
      #   print("dict does NOT have key top")
      #   arts = []
      #   arts.append(a)
      #   arts_cache[key] = arts
      #   print("check dict after 1st item", arts_cache.items())
      # elif key in arts_cache:
      #   print("dict HAS key top", arts_cache.items())
      #   arts = arts_cache[key]
      #   arts.append(a)
      #   arts_cache[key] = arts

      # redirect to that specific art blog
      self.redirect("/")

    else:
      error = "We need both title and artwork!"
      self.render_front(title=title, art=art, error=error)


app = webapp2.WSGIApplication(
    [
        ("/", MainPage),
    ],
    debug=True,
)
