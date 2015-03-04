# -*- coding: utf-8 -*-
from libs.handlers import *
from db.models import *
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import logging
from datetime import timedelta, datetime

from blob_utils import core
from google.appengine.api import files, images
import random

class MainPage(DirectHandler):
    def get(self):
        bookmarks = Bookmark.query().order(-Bookmark.build_time).fetch()
        self.HtmlResponse('BackendPage.html', {'bookmarks': bookmarks})

class AddBookmark(DirectHandler):
    def post(self):
        #key_id = self.request.get('key_id')
        url = self.request.get('url')
        title = self.request.get('title')
        desc = self.request.get('desc')
        desc = desc.replace('\n', '<br/>')
        tags = self.request.get('tags')
        upload_result_urls = []

        import re
        for name, fieldStorage in self.request.POST.items():
            #logging.info(name) --> 欄位名稱
            #logging.info(fieldStorage) --> 欄位內容(值或是檔案), 檔案print 出來類似 FieldStorage(u'image_files', u'105705.jpg')

            if type(fieldStorage) is not unicode:
                #logging.info(fieldStorage.file) --> ex: <cStringIO.StringO object at 0xfbc1fba0>

                result = {}
                result['name'] = re.sub(
                    r'^.*\\',
                    '',
                    fieldStorage.filename
                )
                result['type'] = fieldStorage.type
                result['size'] = self.get_file_size(fieldStorage.file)

                blob_key = str(
                    self.write_blob(fieldStorage.value, result)
                )

                upload_result_urls.append(images.get_serving_url(blob_key))

        Bookmark.add_item(title=title, url=url, desc=desc, tags=tags, thumb_urls=upload_result_urls)

        self.redirect('/')