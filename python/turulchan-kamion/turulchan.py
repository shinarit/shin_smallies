#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""This module allow you to post to Kusaba X imageboards.
Only tested with Turulchan, no captcha support.
"""

import urllib2
import urllib
import htmllib
import re
import cookielib
from util import *

def Post(board, reply, _file, cookies, name, email, text, password = 'kamion', proxy = None, max_size = "2560000", url = "http://turulchan.net/board.php"):
    """Post to imageboard. 
    cookies should be a CookieJar from cookielib, or eqvivalent."""
    if str(reply)=='0': return False
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    if proxy:
        opener.add_handler(urllib2.ProxyHandler({'http':proxy}))
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    params={'board':board, 'replythread':reply, 'MAX_FILE_SIZE': max_size,  
  "email":'', "name":name, 'em':email, 'message':text, 'postpassword':password}
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies),
                                  MultipartPostHandler)
    if proxy:
        opener.add_handler(urllib2.ProxyHandler({'http':proxy}))
    if (_file):
        params['imagefile']=open(_file, "rb")
    return opener.open(url, params).read()

def GetMaxSize(board, cookies, proxy = None, url = "http://turulchan.net/%s/"):
    """Get board's maximum supported file size.
    cookies should be a CookieJar from cookielib, or eqvivalent.
    proxy format is IP:PORT"""
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    if proxy:
        opener.add_handler(urllib2.ProxyHandler({'http':proxy}))
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    page = opener.open(url%board).read()
    return page.split('<input type="hidden" name="MAX_FILE_SIZE" value="')[1].split('" />')[0]
