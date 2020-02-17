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
import jinja2
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import memcache
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

template_dir = os.path.join(os.path.dirname(__file__), "templates")
# set the jinjia2 environment and tell where it goes to look for template file
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


def get_blog_url(blog):
  return '/aria/%s' % blog.key.id()


def render(handler, template, **kw):
  t = jinja_env.get_template(template)
  output = t.render(kw)
  handler.response.out.write(output)


class Blog(ndb.Model):
  title = ndb.StringProperty(required=True)
  article = ndb.TextProperty(required=True)
  photo_key = ndb.BlobKeyProperty()
  photo_url = ndb.StringProperty()
  created = ndb.DateTimeProperty(auto_now_add=True)


class FrontPage(webapp2.RequestHandler):

  def get(self):
    blogs = ndb.gql("select * from Blog order by created desc limit 10")
    upload_url = blobstore.create_upload_url('/upload_photo')
    render(
        self,
        "aria_frontpage.html",
        blogs=blogs,
        upload_url=upload_url,
        get_blog_url=get_blog_url)


class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
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
      render(
          self,
          "aria_frontpage.html",
          title=title,
          article=article,
          error=error,
      )

    blog = self._make_blog()
    blog_key = blog.put()
    self.redirect("/aria/%s" % (blog_key.id()))


class BlogPage(webapp2.RequestHandler):

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
    render(self, "aria_blogpage.html", blog=blog)


app = webapp2.WSGIApplication(
    [
        ("/", FrontPage),
        ('/upload_photo', PhotoUploadHandler),
        ("/aria/([0-9]+)", BlogPage),
    ],
    debug=True,
)
