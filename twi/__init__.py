#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from twython import Twython

from .models import (
    DBSession,
    PostedTweets,
)



class Twi(object):
    def __init__(self, app_key, app_secret, oauth_token, oauth_token_secret, slack_channel, search_term):
        self.twitter = Twython(
            app_key,
            app_secret,
            oauth_token,
            oauth_token_secret
        )

        self.search_term = search_term
        self.slack_channel = slack_channel

    def load_tweets(self):
        result = self.twitter.search(q=self.search_term)
        return result['statuses']

    def get_next_tweet(self):
        tweets = self.load_tweets()
        for tweet in tweets:
            if not PostedTweets.tweet_was_posted(tweet['id_str'], self.slack_channel):
                link = 'https://twitter.com/' + tweet['user']['screen_name'] + '/status/' + tweet['id_str']
                text = tweet['text']
                ts = time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')

                PostedTweets.processing_tweet(tweet, self.search_term, self.slack_channel)

                for ext_link in tweet['entities']['urls']:
                    text = text.replace(ext_link['url'], ext_link['expanded_url'])

                return {
                    'text': '',
                    'attachments': [{
                        'fallback': text,
                        'color': '#0084B4',
                        'pretext': '',
                        'author_name': tweet['user']['name'],
                        'author_link': 'https://twitter.com/' + tweet['user']['screen_name'],
                        'author_icon': tweet['user']['profile_image_url_https'],
                        'title': link,
                        'title_link': link,
                        'text': text,
                        'footer': 'Twitter',
                        'footer_icon': 'https://abs.twimg.com/icons/apple-touch-icon-192x192.png',
                        'ts': time.mktime(ts),
                    }]
                }
        return None
