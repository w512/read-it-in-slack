#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from settings import DB_ENGINE



Base = declarative_base()

class PostedTweets(Base):
    __tablename__ = 'PostedTweets'
    id = Column(Integer, primary_key=True)
    tweets_id = Column(String)
    channel_name = Column(String)
    search_term = Column(String)
    post_date = Column(DateTime)

    UniqueConstraint(tweets_id, channel_name)

    @classmethod
    def save_tweet_info(cls, tweet, search_term, channel_name):
        db_session = DBSession()
        new_entry = cls(
            tweets_id = tweet['id_str'],
            channel_name = channel_name,
            search_term = search_term,
            post_date = datetime.datetime.utcnow(),
        )
        db_session.add(new_entry)
        db_session.commit()
        db_session.close()

    @classmethod
    def tweet_was_posted(cls, tweet_id, channel_name):
        db_session = DBSession()
        tweet_from_db = db_session.query(cls.tweets_id).filter(
            cls.tweets_id == tweet_id,
            cls.channel_name == channel_name,
        ).one_or_none()
        db_session.close()
        if tweet_from_db:
            return True
        return False


class PostedRssEntry(Base):
    __tablename__ = 'PostedRssEntry'
    id = Column(Integer, primary_key=True)
    entry_link = Column(String)
    source = Column(String)
    channel_name = Column(String)
    post_date = Column(DateTime)

    UniqueConstraint(entry_link, channel_name)

    @classmethod
    def save_entry_info(cls, entry_link, source, channel_name):
        db_session = DBSession()
        new_entry = cls(
            entry_link = entry_link,
            source = source,
            channel_name = channel_name,
            post_date = datetime.datetime.utcnow(),
        )
        db_session.add(new_entry)
        db_session.commit()
        db_session.close()

    @classmethod
    def entry_was_posted(cls, entry_link, channel_name):
        db_session = DBSession()
        entry_from_db = db_session.query(cls.entry_link).filter(
            cls.entry_link == entry_link,
            cls.channel_name == channel_name,
        ).one_or_none()
        db_session.close()
        if entry_from_db:
            return True
        return False


engine = create_engine(DB_ENGINE)
Base.metadata.bind = engine
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
