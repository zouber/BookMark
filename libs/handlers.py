# -*- coding: utf-8 -*-
import os
import urllib
import webapp2
import jinja2
import logging
#import sys
import re

def datetimeformat(datetime):
    # 參考 http://mymissionlog.blogspot.tw/2015/01/google-app-engine.html
    #logging.info( type(datetime.strftime('%Y/%m/%d') ) )
    #return datetime.strftime('%Y/%m/%d')

    return str(datetime.year) + u'年' + str(datetime.month) + u'月' + str(datetime.day) + u'日'

def transfer_single_url_into_hyperlink(match_gp):
    url = match_gp.group(0)
    return '<a href="%s" target="_blank" class="content_hyperlink">%s</a>' % (url, url)

def url_to_hyperlink(content):
    return re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', transfer_single_url_into_hyperlink, content)

def br_to_slash_n(content):
    return content.replace('<br/>', '\n')
    
def datetimeformat_withhour(datetime):
    if datetime.hour == 0 and datetime.minute == 0:
        return str(datetime.year) + u'年' + str(datetime.month) + u'月' + str(datetime.day) + u'日'
    else:
        return str(datetime.year) + u'年' + str(datetime.month) + u'月' + str(datetime.day) + u'日 ' + '%02d' % datetime.hour + u'：' + '%02d' % datetime.minute

def convert_image_url(url, frame_size):
    if 'ggpht.com' in url:
        return url + '=s%s' % frame_size
    else:
        return url

JINJA_ENVIRONMENT = jinja2.Environment(
    #loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    loader=jinja2.FileSystemLoader('template'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

JINJA_ENVIRONMENT.filters['datetimeformat'] = datetimeformat
JINJA_ENVIRONMENT.filters['datetimeformat_withhour'] = datetimeformat_withhour
JINJA_ENVIRONMENT.filters['br_to_slash_n'] = br_to_slash_n
JINJA_ENVIRONMENT.filters['convert_image_url'] = convert_image_url
JINJA_ENVIRONMENT.filters['url_to_hyperlink'] = url_to_hyperlink

class DirectHandler(webapp2.RequestHandler):
    def get_host(self):
        from urlparse import urlparse
        return urlparse(self.request.url).netloc

    def HtmlResponse(self, template_name, template_values):
        self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        logging.info(os.path.dirname(__file__))
        #template_path = os.path.join(os.path.dirname(__file__), 'template', template_name)
        template_path = template_name
        template = JINJA_ENVIRONMENT.get_template(template_path)
        template_values['host'] = self.request.host
        self.response.write(template.render(template_values))

    def JsonResponse(self, status, value):
        import json

        callback = self.request.get("callback")

        value['status'] = status
        value['callback'] = callback
        # http://webapp-improved.appspot.com/guide/request.html#common-request-attributes
        value['host'] = self.request.host
        logging.info('host url: %s' % self.request.host_url)

        self.response.headers["Content-Type"] = "application/x-javascript"
        
        if callback:
            self.response.write("%s(%s)" % (callback, json.dumps(value, indent=4, sort_keys=True, separators=(',', ': '))))
        else:
            self.response.headers["Content-Type"] = "application/json"
            self.response.out.write(json.dumps(value, indent=4, sort_keys=True, separators=(',', ': ')))
            # don't raise "Internal Server Error(500)" when encounter status == False
            #if not status:
            #    self.response.set_status(500)