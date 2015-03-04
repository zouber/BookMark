import webapp2
from google.appengine.ext.webapp import blobstore_handlers
import logging

class Upload(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        logging.info('test')
        blob_key = str(self.get_uploads('default')[0].key())
        logging.info(blob_key)
        self.response.out.write(blob_key)

app = webapp2.WSGIApplication([
    ('.*',  Upload),
])