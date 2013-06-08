# -*- coding: utf-8 -*-

import unittest
from nose.tools import nottest, istest, raises,eq_,ok_

from ezlog2.model import Tweet,User
from ezlog2.model.comment import Comment
from ezlog2.model.message import NotifyMessage
from common import user_create,tweet_create

class TestComment(unittest.TestCase):
    def setUp(self):
        self.user    = user_create("fake","12","fakeone")
        self.tweet   = tweet_create("this is a test")
        self.comment = Comment.add("comment2",self.tweet,self.user)

    def test_create_comment(self):
        eq_(Tweet.objects().count(),1)

    def test_get_comments_bytweetid(self):
        comments = Comment.get_comments_bytweetid(self.tweet.id)
        eq_(comments[0],self.comment)

    def tearDown(self):
        User.drop_collection()
        Tweet.drop_collection()
        Comment.drop_collection()
        NotifyMessage.drop_collection()
