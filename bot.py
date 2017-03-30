#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import _thread

from slackclient import SlackClient

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

from twi import Twi



class Bot(object):
    def __init__(self):
        self.twi = Twi(
            TWITTER_APP_KEY,
            TWITTER_APP_SECRET,
            TWITTER_OAUTH_TOKEN,
            TWITTER_OAUTH_TOKEN_SECRET,
            SLACK_CHANNEL,
        )

        self.client = SlackClient(
            SLACK_API_TOKEN,
            bot_icon=SLACK_BOT_ICON,
            bot_emoji=SLACK_BOT_EMOJI
        )

        self.selected_chanel = self.client.find_channel_by_name(SLACK_CHANNEL)

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
            tweet = self.twi.get_next_tweet()
            if tweet:
                self.client.send_message(
                    self.selected_chanel,
                    tweet['text'],
                    tweet['attachments'],
                )
            time.sleep(10)
























