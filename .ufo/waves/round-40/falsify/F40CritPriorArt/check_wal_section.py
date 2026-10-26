#!/usr/bin/env python3
"""F40CritPriorArt check D: locate the entry's wal.html §4 sentence and its section.
Usage: check_wal_section.py <wal.html>   -> prints one CHECK D line."""
import re, sys

h = open(sys.argv[1], encoding='utf8', errors='replace').read()
heads = [(m.start(), re.sub(r'\s+', ' ', re.sub('<[^>]+>', '', m.group(1))).strip())
         for m in re.finditer(r'<h1[^>]*>(.*?)</h1>', h, re.S)]
m = re.search('deleted automatically', h)
if not m:
    print('CHECK D    FAIL wal.html sentence absent')
    raise SystemExit
sec = [t for p, t in heads if p < m.start()][-1]
text = re.sub(r'\s+', ' ', re.sub('<[^>]+>', '', h))
q = ('Usually, the WAL file is deleted automatically when the last '
     'connection to the database closes.')
print(('CHECK D    PASS wal.html carries the sentence verbatim in "' + sec + '"')
      if q in text else 'CHECK D    FAIL sentence not contiguous after tag strip')
