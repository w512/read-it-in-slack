#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import _thread

from twython import Twython

from  slackclient import SlackClient

from settings import (
    SLACK_API_TOKEN,
    SLACK_BOT_ICON,
    SLACK_BOT_EMOJI,
    SLACK_CHANNEL,

    TWITTER_APP_KEY,
    TWITTER_APP_SECRET,
    TWITTER_OAUTH_TOKEN,
    TWITTER_OAUTH_TOKEN_SECRET
)



class Bot(object):
    def __init__(self):
        self.client = SlackClient(
            SLACK_API_TOKEN,
            bot_icon=SLACK_BOT_ICON,
            bot_emoji=SLACK_BOT_EMOJI
        )

        self.selected_chanel = self.client.find_channel_by_name(SLACK_CHANNEL)

        self.twitter = Twython(
            TWITTER_APP_KEY,
            TWITTER_APP_SECRET,
            TWITTER_OAUTH_TOKEN,
            TWITTER_OAUTH_TOKEN_SECRET
        )

        self.dispatched_tweets_ids = []

    def run(self):
        self.client.rtm_connect()
        _thread.start_new_thread(self.keepactive, tuple())
        self.loop()

    def keepactive(self):
        while True:
            time.sleep(30 * 60)
            self.client.ping()

    def loop(self):
        while True:
            events = self.client.rtm_read()
            # for event in events:
            #     if event.get('type') != 'message':
            #         continue
            tweet = self.get_next_tweet()
            if tweet:
                self.client.send_message(
                    self.selected_chanel,
                    tweet['text'],
                    tweet['attachments'],
                )
            time.sleep(5)

    def load_tweets(self):
        result = self.twitter.search(q='"Python developer"')
        return result['statuses']

    def get_next_tweet(self):
        tweets = self.load_tweets()
        for tweet in tweets:
            if tweet['id'] not in self.dispatched_tweets_ids:
                self.dispatched_tweets_ids.append(tweet['id'])

                link = 'https://twitter.com/' + tweet['user']['screen_name'] + '/status/' + tweet['id_str']
                ts = time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')

                return {
                    'text': '',
                    'attachments': [{
                        'fallback': tweet['text'],
                        'color': '#0084B4',
                        'pretext': '',
                        'author_name': tweet['user']['name'],
                        'author_link': 'https://twitter.com/' + tweet['user']['screen_name'],
                        'author_icon': tweet['user']['profile_image_url_https'],
                        'title': link,
                        'title_link': link,
                        'text': tweet['text'],
                        'footer': 'Twitter',
                        'footer_icon': 'https://abs.twimg.com/icons/apple-touch-icon-192x192.png',
                        'ts': time.mktime(ts),
                    }]
                }
        return None






















