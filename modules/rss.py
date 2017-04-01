#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import feedparser

from .models import (
    DBSession,
    PostedRssEntry,
)



class Rss(object):
    def __init__(self, feeds, slack_channel):
        self.feeds = feeds
        self.slack_channel = slack_channel

    def load_feeds(self):
        entries = []
        for feed in self.feeds:
            result = feedparser.parse(feed['url'])
            for entry in result['entries']:
                entry['name'] = feed['name']
                entry['source'] = feed['url']
            entries.extend(result['entries'])
        return entries

    def get_next_entries(self):
        entries_for_posting = []
        entries = self.load_feeds()
        for entry in entries:
            if not PostedRssEntry.entry_was_posted(entry['link'], self.slack_channel):
                PostedRssEntry.save_entry_info(entry['link'], entry['source'], self.slack_channel)
                entries_for_posting.append({
                    'text': '',
                    'attachments': [{
                        'fallback': '{0}\n{1}'.format(entry['title'], entry['link']),
                        'color': '#36A64F',
                        'author_name': entry['name'],
                        'title': entry['title'],
                        'title_link': entry['link'],
                    }]
                })
        return entries_for_posting
