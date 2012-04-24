#!/usr/bin/env python

import sys
import twitter
import operator
from dateutil.parser import parse

__author__ = 'Irving Y. Ruan <irvingruan@gmail.com'
__version__ = '0.1'

twitterURL = 'http://twitter.com'

def fetch(user):
    data = {}
    api = twitter.Api()
    max_id = None
    total = 0
    while True:
        statuses = api.GetUserTimeline(user, count=200, max_id=max_id)
        newCount = ignCount = 0
        for s in statuses:
            if s.id in data:
                ignCount += 1
            else:
                data[s.id] = s
                newCount += 1
        total += newCount
        print >> sys.stderr, "Fetched %d/%d/%d new/old/total." % (
            newCount, ignCount, total)
        if newCount == 0:
            break
    
        
    return data.values()

def htmlPrint(user, tweets):
    for t in tweets:
        t.pdate = parse(t.created_at)
        
    key = operator.attrgetter('pdate')
    tweets = sorted(tweets, key=key)
    f = open('%s.html' % user, 'wb')
    print >>f, """<html><title>Tweets for %s</title>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
    <body><small>""" % user
    for i, t in enumerate(tweets):
        print >>f, '%d. %s <a href="%s/%s/status/%d">%s</a><br/>' % (
            i, t.pdate.strftime('%Y-%m-%d %H:%M'), twitterURL,
            user, t.id, t.text.encode('utf8'))
    print >>f, '</small></body></html>'
    f.close()
    
if __name__ == '__main__':
    user = "irvingruan" if len(sys.argv) < 2 else sys.argv[1]
    data = fetch(user)
    htmlPrint(user, data)