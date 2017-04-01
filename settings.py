#!/usr/bin/env python3
# -*- coding: utf-8 -*-


SLACK_BOT_ICON = 'http://lorempixel.com/output/cats-q-c-64-64-3.jpg'
SLACK_BOT_EMOJI = ':godmode:'
SLACK_CHANNEL = 'general'


DB_ENGINE = 'sqlite:///modules/db.sqlite'

SEARCH_TERM = 'sale'

FEEDS = [
    {
        'name': 'Nikolay\'s Blog',
        'url': 'https://blokhin.us/rss/',
    },
    {
        'name': 'Planet Python',
        'url': 'http://planetpython.org/rss20.xml',
    },
]


try:
    from local_settings import *
except ImportError:
    print('ERROR: There is no local_settings.py!')

