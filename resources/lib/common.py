#!/usr/bin/python
# -*- coding: utf-8 -*-
from xbmcswift2 import xbmc
import urllib2
import gzip
import StringIO
import re
import traceback


def colorize(label, color):
    return "[COLOR %s]" % color + label + "[/COLOR]"


def GetHttpData(url, data=None, cookie=None):

    xbmc.log("Fetch URL :%s, with data: %s" % (url, data))
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) {0}{1}'.
                       format('AppleWebKit/537.36 (KHTML, like Gecko) ',
                              'Chrome/28.0.1500.71 Safari/537.36'))
        req.add_header('Accept-encoding', 'gzip')
        if cookie is not None:
            req.add_header('Cookie', cookie)
        if data:
            response = urllib2.urlopen(req, data, timeout=3)
        else:
            response = urllib2.urlopen(req, timeout=3)
        httpdata = response.read()
        if response.headers.get('content-encoding', None) == 'gzip':
            httpdata = gzip.GzipFile(fileobj=StringIO.StringIO(httpdata)).read()
        response.close()
        match = re.compile('encoding=(.+?)"').findall(httpdata)
        if not match:
            match = re.compile('meta charset="(.+?)"').findall(httpdata)
        if match:
            charset = match[0].lower()
            if (charset != 'utf-8') and (charset != 'utf8'):
                httpdata = unicode(httpdata, charset).encode('utf8')
    except Exception:
        print_exc()
        httpdata = '{"status": "Fail"}'
    return httpdata


def print_exc():
    traceback.print_exc()
