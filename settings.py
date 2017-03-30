#!/usr/bin/env python3
# -*- coding: utf-8 -*-


SLACK_API_TOKEN = ''
SLACK_BOT_ICON = ''
SLACK_BOT_EMOJI = ''
SLACK_CHANNEL = ''


TWITTER_APP_KEY = ''
TWITTER_APP_SECRET = ''
TWITTER_OAUTH_TOKEN = ''
TWITTER_OAUTH_TOKEN_SECRET = ''


DB_ENGINE = None


try:
    from local_settings import *
except ImportError:
    print('WARNING: There is no local_settings.py!')

