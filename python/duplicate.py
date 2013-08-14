#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import hashlib
import threading

NUM_OF_THREADS = 8

hashes = {}

class hashChecker(threading.Thread):
  def __init__(self, filename):
    threading.Thread.__init__(self)
    self.filename = filename
  
  def run(self):
    global hashes
    with open(self.filename, 'rb') as f:
      data = f.read()
    md5 = hashlib.md5(data)
    hash = md5.digest()
    if hash in hashes:
      hashes[hash].append(file)
    else:
      hashes[hash] = [file]


path = sys.argv[1]
delete = len(sys.argv) > 2

files = [ os.path.join(path, file) for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)) ]

for file in files:
  t = hashChecker(file)
  t.start()

mainthread = threading.current_thread()
threads = threading.enumerate()
while len(threads) > 1:
  if mainthread == threads[0]:
    threads[-1].join()
  else:
    threads[0].join()
  threads = threading.enumerate()

found = False
for lists in hashes.itervalues():
  if len(lists) > 1:
    found = True

    print "Duplicate found: ", '\n', '\t\n'.join(lists)

    if delete:
      for todel in lists[1:]:
        try:
          os.remove(todel)
          print "Deleted: ", todel
        except:
          print "Could not delete: ", todel

if not found:
  print "No duplicates found"
