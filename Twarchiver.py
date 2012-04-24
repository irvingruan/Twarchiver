#!/usr/bin/env python

"""
Copyright (c) 2012 Irving Y. Ruan <irvingruan@gmail.com>

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,    
      this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

__author__ = 'Irving Y. Ruan <irvingruan@gmail.com'
__version__ = '0.1b'

import sys
import twitter
import operator
from dateutil.parser import parse

twitter_base_url = 'http://twitter.com'
tweets_data = {}

def get_tweets(username):
    """
        Returns a list of tweets.
        
        Args:
            username: The username to get tweets for. If the user is protected, authentication will be required with the owner's credentials.
            
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