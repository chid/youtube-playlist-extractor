#f = open("test.html")
#HTML = f.read()
import urllib2
response = urllib2.urlopen('http://www.youtube.com/playlist?list=PL772556F1EFC4D01C')
HTML = response.read()
import re

# http://www.youtube.com/watch?v=3_RhISgoXUs&list=PLED25F943F8D6081C&index=11&feature=plpp_video
for i in re.findall(r"http://www\.youtube\.com/watch[^\\&]*", HTML):
  print type(i)

n = 0
for i in re.findall(r"/watch\?v=[a-zA-Z0-9\-_]+", HTML):
  print "http://www.youtube.com"+i
  n = n + 1

import sys
sys.stderr.write('%s files found \n' % n)
