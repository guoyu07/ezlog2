# -*- coding: utf-8 -*-

import unittest
from nose.tools import nottest, istest, raises,eq_,ok_

from ezlog2.model import User
from ezlog2.model.user import Admin,Follow
from ezlog2.util import sha224
from .common import user_create

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user   = user_create("fake","12","fakeone")

    #this user only test for follow relationship
    @nottest
    def _set_up_followed_user(self):
        self.followed_user = user_create("followed_fake",
                                         "cc12",
                                         "1fakeone")
        Follow.toggle_follow(self.user.id,self.followed_user.id)

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

    def test_get_user_by_nickname(self):
        user    = User.get_users_startwith("1")[0]
        eq_(user,self.user)

    def test_is_following(self):
        self._set_up_followed_user()
        ok_(self.user.is_following(self.followed_user.id))

    def test_get_followers(self):
        self._set_up_followed_user()
        user    = self.followed_user.get_followers()[0]
        eq_(user,self.user)

    def test_get_following_users(self):
        self._set_up_followed_user()
        user    = self.user.get_following_users()[0]
        eq_(user,self.followed_user)

    def test_can_send_pm(self):
        self._set_up_followed_user()
        ok_(not self.user.can_send_pm_to_user(self.followed_user))
        ok_(not self.followed_user.can_send_pm_to_user(self.user))
        Follow.toggle_follow(self.followed_user.id,self.user.id)
        ok_(self.user.can_send_pm_to_user(self.followed_user))
        ok_(self.followed_user.can_send_pm_to_user(self.user))

    def test_follower_counter(self):
        self._set_up_followed_user()
        eq_(self.followed_user.follower_counter,1)

    def test_following_counter(self):
        self._set_up_followed_user()
        eq_(self.user.following_counter,1)

    def tearDown(self):
        User.drop_collection()
        Follow.drop_collection()

class TestAdmin(unittest.TestCase):
    def setUp(self):
        self.admin   = Admin(email="fake",
                           password=sha224("fakeone")).save()
    def test_auth(self):
        ok_(Admin.is_valid("fake",sha224("fakeone")))
        admin = Admin.validate_user("fake",sha224("fakeone"))
        eq_(admin.id,self.admin.id)

    def tearDown(self):
        Admin.drop_collection()






