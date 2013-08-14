#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import hashlib

def makeHash(filepath):
  return 0

path = sys.argv[1]
delete = False
if len(sys.argv) > 2:
  delete = bool(sys.argv[2])
files = [ os.path.join(path, file) for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)) ]

hashes = {}

for file in files:
  with open(file, 'rb') as f:
    data = f.read()
  md5 = hashlib.md5(data)
  hash = md5.digest()
  if hash in hashes:
    hashes[hash].append(file)
  else:
    hashes[hash] = [file]

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
