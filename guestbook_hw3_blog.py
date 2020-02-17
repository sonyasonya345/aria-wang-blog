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


class BlogHandler(webapp2.RequestHandler):

  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))


def render_str(template, **params):
  t = jinja_env.get_template(template)
  return t.render(params)


class Post(db.Model):
  subject = db.StringProperty(required=True)
  content = db.TextProperty(required=True)
  created = db.DateTimeProperty(auto_now_add=True)
  last_modified = db.DateTimeProperty(auto_now=True)

  def render(self):
    self._render_text = self.content.replace('\n', '<br>')
    return render_str("post.html", p=self)


class BlogFront(BlogHandler):

  def get(self):
    posts = db.GqlQuery("select * from Post order by created desc limit 10")
    self.render("blog_front.html", posts=posts)


def blog_key(name="default"):
  return db.Key.from_path("blogs", name)


class PostPage(BlogHandler):

  def get(self, post_id):
    key = db.Key.from_path("Post", int(post_id), parent=blog_key())
    post = db.get(key)

    if not post:
      self.error(404)
      return

    self.render("permalink.html", post=post)


# NewPost is used to:
# 1) give user a form to create new post
# 2) process the submit form: 1) create the instance and redirect the user to that post link
class NewPost(BlogHandler):

  def get(self):
    self.render("newpost.html")

  def post(self):
    subject = self.request.get("subject")
    content = self.request.get("content")

    if subject and content:
      # create an instance of Art;
      # use object_art.put() method store the art object/instance into the database
      p = Post(parent=blog_key(), subject=subject, content=content)
      p.put()
      self.redirect("/blog/%s" % str(p.key().id()))

    else:
      error = "We need both subject and content!"
      self.render("newpost.html", subject=subject, content=content, error=error)


app = webapp2.WSGIApplication(
    [
        ("/blog/?", BlogFront),
        ("/blog/([0-9]+)", PostPage),
        ("/blog/newpost", NewPost),
    ],
    debug=True,
)
