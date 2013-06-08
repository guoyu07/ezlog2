# -*- coding: utf-8 -*-

import unittest
from nose.tools import nottest, istest, raises,eq_,ok_

from ezlog2.model import Tweet
from ezlog2.model.search import DocItem,SearchIndex
from common import tweet_create

class TestSearch(unittest.TestCase):
    def setUp(self):
        self.tweet1 = tweet_create(u"这是一个测试")
        self.tweet2 = tweet_create(u"测试一下搜索")
        SearchIndex.build_index()

    def test_builder_index(self):
        ok_(SearchIndex.objects().count()>0)

    def test_get_tweets_by_keywords(self):
        tweets = SearchIndex.get_tweets_by_keywords([u"测试"])
        eq_(len(tweets),2)
        tweets = SearchIndex.get_tweets_by_keywords([u"这是", u"测试"])
        eq_(tweets[0],self.tweet1)

    def tearDown(self):
        Tweet.drop_collection()
        SearchIndex.drop_collection()
