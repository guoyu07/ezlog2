# -*- coding: utf-8 -*-

import unittest
from nose.tools import nottest, istest, raises,eq_,ok_

from ezlog2.model.message import NotifyMessage,PrivateMessage

class TestNotifyMessage(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        NotifyMessage.drop_collection()
        


class TestPrivateMessage(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass