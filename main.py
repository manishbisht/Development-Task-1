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

import webapp2
import jinja2
import os
import urllib2
import runpy
import sys
from google.appengine.api import app_identity
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class MainPage(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def get(self):
        upload_url = blobstore.create_upload_url('/upload')
        self.render('home.html', upload_url=upload_url)

        '''self.response.out.write("""
        <html><body>
        <form action="{0}" method="POST" enctype="multipart/form-data">
          Upload File: <input type="file" name="file"><br>
          <input type="submit" name="submit" value="Submit">
        </form>
        </body></html>""".format(upload_url))'''


class UploadImage(MainPage, blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload = self.get_uploads()[0]
        self.redirect('download/' + str(upload.key()))


class SaveImageToServer(MainPage):
    def get(self, photo_key):
        server_url = app_identity.get_default_version_hostname()
        image_data = urllib2.urlopen('http://' + server_url + '/view/' + photo_key)
        image_data = image_data.read()
        upload_url = os.getcwd() + '/upload/' + photo_key
        f = open(upload_url, 'a')
        f.write(image_data)
        f.close()
        self.redirect('/analyse/' + photo_key)


class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, photo_key):
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            self.send_blob(photo_key)


class ProcessImage(MainPage):
    def get(self, photo_key):
        #execfile('compute.py')
        sys.argv = ['', 'data/*.png']
        runpy.run_path('./compute.py', run_name='__main__')
        #self.response.out.write(subprocess.__file__)
        #sys.argv.append('')
        #os.system("./processin.sh")
        #self.response.out.write(os.getcwd())
        #subprocess.call(['processing.sh upload/%s' (photo_key)])
        #execfile('./processing.sh')
        #subprocess.call(["processing.sh", "upload/"+photo_key])

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/upload', UploadImage),
    ('/view/([^/]+)?', ViewPhotoHandler),
    ('/download/([^/]+)?', SaveImageToServer),
    ('/analyse/([^/]+)?', ProcessImage)
], debug=True)
