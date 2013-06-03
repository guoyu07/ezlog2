# -*- coding: utf-8 -*-

import unittest
from nose.tools import nottest, istest, raises,eq_,ok_

from ezlog2.model import Tweet
from ezlog2.model.message import NotifyMessage
from common import user_create,tweet_create



class TestTweet(unittest.TestCase):

    def setUp(self):
        self.tweet = tweet_create("this is a test")

    def test_create_tweet(self):
        eq_(Tweet.objects().count(),1)

    def test_retweet(self):
        pass

    def test_is_retweet(self):
        ok_(not self.tweet.is_retweet())

    def test_original_tweet(self):
        eq_(self.tweet.original_tweet,None)

    def test_get_tweet_by_id(self):
        tweet   = Tweet.get_tweet_byid(self.tweet.id)
        eq_(tweet,self.tweet)

    def tearDown(self):
        Tweet.drop_collection()
        NotifyMessage.drop_collection()





