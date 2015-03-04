# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from datetime import timedelta, datetime
import logging

def generate_sn(cls):
    try:
        item = cls.query().order(-cls.sn).fetch(1)
        if len(item) > 0:
            item = item[0]
            current_sn = int(item.sn)
            # 20 digits total
            new_sn = '%020d' % (current_sn + 1)
        else:
            return '0'*20
    except:
        return None

class Bookmark(ndb.Model):
    sn = ndb.StringProperty(required=True)
    url = ndb.StringProperty(required=True, default='http://www.google.com')
    title = ndb.StringProperty(required=True, default=u'Google 首頁')
    desc = ndb.TextProperty()
    tags = ndb.StringProperty(repeated=True)
    author = ndb.StringProperty(default='zouber')
    thumb_urls = ndb.StringProperty(repeated=True)
    access_time = ndb.DateTimeProperty(auto_now=True)
    build_time = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def add_item(cls, **args):
        new_sn = generate_sn(cls)

        item_data = {'url': '', 'title': '', 'desc': '', 'tags': '', 'thumb_urls': ''}

        for index in item_data:
            if args.has_key(index):
                if index == 'tags' or index == 'thumb_urls':
                    if len(args[index]) == 0:
                        item_data[index] = []
                    else:
                        item_data[index] = args[index].split(',')
                else:
                    item_data[index] = args[index]
                


        item = cls(sn=new_sn,
              url=item_data['url'],
              title=item_data['title'],
              desc=item_data['desc'],
              tags=item_data['tags'],
              thumb_urls=item_data['thumb_urls'])

        item.put()
