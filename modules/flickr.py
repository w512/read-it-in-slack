#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import feedparser

from .models import (
    DBSession,
    PostedFlickrPhoto,
)



class Flickr(object):
    def __init__(self, tags, slack_channel):
        self.slack_channel = slack_channel
        self.tags = tags
        self.url = 'https://api.flickr.com/services/feeds/photos_public.gne?tagmode=all&tags=' + ','.join(tags)

    def load_feed(self):
        photos = []
        result = feedparser.parse(self.url)
        for entry in result['entries']:
            photo_direct_link = ''
            photo_web_link = ''
            for link in entry['links']:
                if link['rel'] == 'enclosure':
                    photo_direct_link = link['href']
                if link['rel'] == 'alternate':
                    photo_web_link = link['href']
            photos.append({
                'title': entry['title'],
                'direct_link': photo_direct_link,
                'web_link': photo_web_link,
                'author_name': entry['author_detail']['name'],
                'author_link': entry['author_detail']['href'],
                'author_avatar': entry['flickr_buddyicon'],
                'published': entry['published'],
            })
        return photos

    def get_next_photos(self):
        photos_for_posting = []
        photos = self.load_feed()
        for photo in photos:
            if not PostedFlickrPhoto.photo_was_posted(photo['direct_link'], self.slack_channel):
                PostedFlickrPhoto.save_photo_info(photo['direct_link'], self.slack_channel)

                ts = time.strptime(photo['published'],'%Y-%m-%dT%H:%M:%SZ')  # '2015-12-24T05:27:01Z'

                photos_for_posting.append({
                    'text': '',
                    'attachments': [{
                        'fallback': photo['direct_link'],
                        'color': '#8c20ba',
                        'author_name': photo['author_name'],
                        'author_link': photo['author_link'],
                        'author_icon': photo['author_avatar'],
                        'image_url': photo['direct_link'],
                        'title': photo['web_link'],
                        'title_link': photo['direct_link'],

                        'footer': 'Flickr',
                        'footer_icon': 'https://s.yimg.com/pw/images/goodies/white-small-circle.png',
                        'ts': time.mktime(ts),
                    }]
                })
        return photos_for_posting
