#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# turulcsen poszt
import urllib2
import urllib
import htmllib
import re
import cookielib
from util import *

def Post(board, reply, _file, cookies, name, email, text, password = 'kamion', proxy = None, max_size = "2560000"):
  if reply=='0': return False
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
  if proxy:
    opener.add_handler(urllib2.ProxyHandler({'http':proxy}))
  opener.addheaders = [('User-agent', 'Mozilla/5.0')]
  #resp=opener.open(url)
  #a=resp.read()
  params={'board':board, 'replythread':reply, 'MAX_FILE_SIZE': max_size,  
  "email":'', "name":name, 'em':email, 'message':text, 'postpassword':password}
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies),
                                MultipartPostHandler)
  if proxy:
    opener.add_handler(urllib2.ProxyHandler({'http':proxy}))
  opener.addheaders = [('User-agent', 'Mozilla/5.0')]
  if (_file):
    params['imagefile']=open(_file, "rb")
  #else: 
  #  params['looong']='' #<-- ez már nem lohere!
  return opener.open('http://turulchan.net/board.php', params).read()

def GetMaxSize(board, cookies, proxy = None):
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
  if proxy:
    opener.add_handler(urllib2.ProxyHandler({'http':proxy}))
  opener.addheaders = [('User-agent', 'Mozilla/5.0')]
  page = opener.open('http://turulchan.net/%s/'%board).read()
  return page.split('<input type="hidden" name="MAX_FILE_SIZE" value="')[1].split('" />')[0]
