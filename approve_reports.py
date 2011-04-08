import http.cookiejar as c
import urllib.request as r
import urllib.parse as p

from pprint import pprint
from urllib.error import HTTPError, URLError

import os
import json
import argparse

parser = argparse.ArgumentParser(description='approve all the reports in a subreddit')
parser.add_argument('--user', '-u', required=True)
parser.add_argument('--password', '-p', required=True)
parser.add_argument('--subreddit', '-s', required=True)
args = parser.parse_args()

loginurl  = "http://www.reddit.com/api/login"
reportsurl  = "http://www.reddit.com/r/%s/about/reports/.json" % args.subreddit
approveurl  = "http://www.reddit.com/api/approve"

# sure, i guess i'll use a cookie jar :|
cj = c.CookieJar()
opener = r.build_opener(r.HTTPCookieProcessor(cj))
r.install_opener( opener )

# login
params = p.urlencode( { 'user': args.user, 'passwd': args.password } )
f = r.urlopen(loginurl, params.encode('utf8'))
f.close()

approved_count = 0

try:
  while True:
    f = r.urlopen(reportsurl)
    reports = json.loads(f.read().decode())
    f.close()

    things = [c['data']['name'] for c in reports['data']['children']]

    # we'll leave if there is nothing
    if len(things) == 0:
      print("nothing left")
      break

    for t in things:
      try:
        params = p.urlencode( { 'id': t, 'uh': reports['data']['modhash'] } )
        f = r.urlopen(approveurl, params.encode('utf8'))
        output = json.loads(f.read().decode())
        f.close()
      except HTTPError as e:
        print("HTTP error %s on %s" % (e.code, t))
      except URLError as e:
        print("URL error %s on %s" % (e.reason, t))
      else:
        print("approved %s" % t)
        approved_count += 1

except:
  pass

print("approved %s things" % approved_count)
