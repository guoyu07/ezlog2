# -*- coding: utf-8 -*-

import unittest
from nose.tools import nottest, istest, raises,eq_,ok_

from ezlog2.model import User
from ezlog2.util import sha224

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user   = User(email="fake",nickname="12",password=sha224("fakeone")).save()

    def test_auth(self):
        ok_(User.is_valid("fake",sha224("fakeone")))
        user = User.validate_user("fake",sha224("fakeone"))
        eq_(user.nickname,self.user.nickname)

    def test_get_user_by_id(self):
        user = User.get_user_by_id(self.user.id)
        eq_(user,self.user)

    def test_email_exist(self):
        ok_(User.is_email_exist("fake"))
        ok_(not User.is_email_exist("fake1"))

    def test_nickname_exist(self):
        ok_(User.is_nickname_exist("12"))
        ok_(not User.is_nickname_exist("e1"))

    def tearDown(self):
        User.drop_collection()








