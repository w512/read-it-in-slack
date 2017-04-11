#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import _thread

from slackclient import SlackClient

import settings
from modules import Twi, Rss, Flickr



class Bot(object):
    def __init__(self, active_plugins):

        self.twi = Twi(
            settings.TWITTER_APP_KEY,
            settings.TWITTER_APP_SECRET,
            settings.TWITTER_OAUTH_TOKEN,
            settings.TWITTER_OAUTH_TOKEN_SECRET,
            settings.SLACK_CHANNEL,
            settings.SEARCH_TERM,
        )

        self.rss = Rss(
            settings.FEEDS,
            settings.SLACK_CHANNEL,
        )

        self.flickr = Flickr(
            settings.FLICKR_TAGS,
            settings.SLACK_CHANNEL,
        )

        self.client = SlackClient(
            settings.SLACK_API_TOKEN,
            bot_icon=settings.SLACK_BOT_ICON,
            bot_emoji=settings.SLACK_BOT_EMOJI
        )

        self.selected_chanel = self.client.find_channel_by_name(
            settings.SLACK_CHANNEL
        )

        self.active_plugins = active_plugins

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

            if self.active_plugins['twitter']:
                tweets = self.twi.get_next_tweets()
                for tweet in tweets:
                    self.client.send_message(
                        self.selected_chanel,
                        tweet['text'],
                        tweet['attachments'],
                    )

            if self.active_plugins['rss']:
                entries = self.rss.get_next_entries()
                for entry in entries:
                    self.client.send_message(
                        self.selected_chanel,
                        entry['text'],
                        entry['attachments'],
                    )

            if self.active_plugins['flickr']:
                photos = self.flickr.get_next_photos()
                for photo in photos:
                    self.client.send_message(
                        self.selected_chanel,
                        photo['text'],
                        photo['attachments'],
                    )

            time.sleep(10)


if __name__ == '__main__':

    active_plugins = {
        'twitter': False,
        'rss': False,
        'flickr': True,
    }

    bot = Bot(active_plugins)
    bot.run()






















