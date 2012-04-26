#!/usr/bin/env python

"""
Copyright (c) 2012 Irving Y. Ruan <irvingruan@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS 
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

__author__ = 'Irving Y. Ruan <irvingruan@gmail.com'
__version__ = '0.1'

import sys
import os
import twitter
import operator
import shutil
from dateutil.parser import parse

twitter_base_url = 'http://twitter.com'
desktop_path = os.path.expanduser('~/Desktop/')

tweets_data = {}

def get_tweets(username):
    """
        Returns a list of tweets.
        
        Args:
            username: The username to get tweets for. If the user is protected authentication will be required with the owner's credentials.
            
        Returns:
            A list of Twitter statuses.
    
    """
    
    global tweets_data
    
    api = twitter.Api()
    max_id = None
    total = 0
    
    while True:
        
        try:
            statuses = api.GetUserTimeline(username, count=200, max_id=max_id)
        except:
            # If Twitter returns any HTTP error, just archive what we have
            generate_html(username, tweets_data.values())
            sys.stdout.write("\nRetrieved a total of %d tweets.\n" % total)
            sys.exit(0)
            
        newCount = ignCount = 0
        for status in statuses:
            if status.id in tweets_data:
                ignCount += 1
            else:
                tweets_data[status.id] = status
                newCount += 1
        total += newCount
        sys.stderr.write("Twarchiver: Retrieved %d new tweets | %d total.\n" % (newCount, total))
        if newCount == 0:
            break
            
        max_id = min([status.id for status in statuses]) - 1
    
    return tweets_data.values()

def generate_html(username, tweets):
    """
        Creates static HTML file with plaintext-style view of your tweets.
    
        Args:
            username: The username of the user for the filename.html.
            tweets: A list of tweets.
    """
    
    for tweet in tweets:
        tweet.pdate = parse(tweet.created_at)
        
    key = operator.attrgetter('pdate')
    tweets = sorted(tweets, key=key, reverse=True)
    
    html_output = open('%s.html' % username, 'wb')
    
    html_output.write("""<html><title>%s's Tweets</title>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
    <body><small>""" % username)
    
    # Write out each status and its corresponding URL
    for index, tweet in enumerate(tweets):
        html_output.write('%d. %s <a href="%s/%s/status/%d">%s</a><br/>' % (
            index, tweet.pdate.strftime('%Y-%m-%d %H:%M'), twitter_base_url,
            username, tweet.id, tweet.text.encode('utf8')))
            
    html_output.write('</small></body></html>')
    html_output.close()
    
    try:
        if os.path.exists(desktop_path + username + '.html'):
            sys.stderr.write(username + '.html already exists. Recreate anyway? (y/n):')
            key = 0
            try:
                key = sys.stdin.read(1)
            except KeyboardInterrupt:
                key = 0

            if key == 'y':
                os.remove(desktop_path + username +'.html')
                shutil.move(os.getcwd() + '/' + username + '.html', desktop_path)
                sys.stderr.write(username + '.html recreated on your Desktop.\n')
            elif key == 'n':
                os.remove(os.getcwd() + '/' + username +'.html') 
            elif key == 0:
                sys.stderr.write("\nError: keyboard interrupted.")
                sys.exit(-1)
        else:
            shutil.move(os.getcwd() + '/' + username + '.html', desktop_path)
            
    except:
        sys.stderr.write("Error: Unable to move %s.html to the Desktop.\n" % username)
        sys.stderr.write("%s.html is located inside this directory.\n" % username)
        sys.exit(-1)
    
def main():
    
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: ./Twarchiver.py <username>\n")
        sys.exit(-1)
    
    username = sys.argv[1]
    tweets_data = get_tweets(username)
    generate_html(username, tweets_data)
    
if __name__ == '__main__':
    main()
    sys.exit(0)