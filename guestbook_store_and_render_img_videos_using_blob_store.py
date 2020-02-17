##############################################
##############################################
#############################################

# Copyright 2015 Google Inc. All rights reserved.
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
"""
Sample application that demonstrates how to use the App Engine Blobstore API.
For more information, see README.md.
"""

# [START gae_blobstore_sample]
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
import webapp2
"""
documentation for blog database: https://cloud.google.com/appengine/docs/standard/python/blobstore/
"""


# This datastore model keeps track of which users uploaded which photos.
class UserPhoto(ndb.Model):
  """
  this class define the UserPhoto entity by what kinds of properties
  """
  user = ndb.StringProperty()
  blob_key = ndb.BlobKeyProperty()


class PhotoUploadFormHandler(webapp2.RequestHandler):
  """
  - blobstore allows user to upload photos or videos through an url or http request
  - users would see a form that allow them to upload the photo/vidoes
  - this form must be "POST" method

  - in the html form, you specific the upload_url
  - the content/vidoes/images would submit to this upload_url
  - this upload_url would have its corresponding handler

  """

  def get(self):
    # [START gae_blobstore_upload_url]
    upload_url = blobstore.create_upload_url('/upload_photo')
    # [END gae_blobstore_upload_url]
    # [START gae_blobstore_upload_form]
    # To upload files to the blobstore, the request method must be "POST"
    # and enctype must be set to "multipart/form-data".
    self.response.out.write("""
<html><body>
<form action="{0}" method="POST" enctype="multipart/form-data">
  Upload File: <input type="file" name="file"><br>
  <input type="submit" name="submit" value="Submit">
</form>
</body></html>""".format(upload_url))
    # [END gae_blobstore_upload_form]


# [START gae_blobstore_upload_handler]
class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  """
  - Then the Blobstore creates a blob from the uploaded content.
  - this blob has a blob key which you can use to refernce or retrieve it later
  - then you can save this blob as an UserPhoto entity, and set its blob_key

  """

  def post(self):
    upload = self.get_uploads()[0]
    user_photo = UserPhoto(
        # user=users.get_current_user().user_id(),
        blob_key=upload.key(),)
    user_photo.put()

    self.redirect('/view_photo/%s' % upload.key())


# [END gae_blobstore_upload_handler]


# [START gae_blobstore_download_handler]
class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):

  def get(self, photo_key):
    if not blobstore.get(photo_key):
      self.error(404)
    else:
      self.send_blob(photo_key)


# [END gae_blobstore_download_handler]

app = webapp2.WSGIApplication([
    ('/', PhotoUploadFormHandler),
    ('/upload_photo', PhotoUploadHandler),
    ('/view_photo/([^/]+)?', ViewPhotoHandler),
],
                              debug=True)
# [END gae_blobstore_sample]