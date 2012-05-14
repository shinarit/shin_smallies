#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import os

def WriteError(msg):
  sys.stderr.write("%s\n" % msg)

def WriteMessage(msg):
  sys.stdout.write("%s\n" % msg)

if len(sys.argv) != 3:
  WriteError("Usage: %s <src> <dst>\nsrc is a regular expression" % sys.argv[0])
  sys.exit(1)

#(?P<id>szoveg)
expr = re.compile(sys.argv[1], re.MULTILINE)

files = os.listdir('.')
subbed = expr.sub(sys.argv[2], '\n'.join(files)).split('\n')

for old, new in zip(files, subbed):
  if old != new:
    WriteMessage("renaming %s to %s" % (old, new))
    os.rename(old, new)

#os.rename(src, dst)

