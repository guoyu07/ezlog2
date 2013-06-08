# -*- coding: utf-8 -*-

import unittest
from nose.tools import nottest, istest, raises,eq_,ok_

from ezlog2.model import User
from ezlog2.model.message import NotifyMessage,PrivateMessage
from .common import user_create

class TestNotifyMessage(unittest.TestCase):
    def setUp(self):
        self.sender   = user_create("s","send","pw")
        self.receiver = user_create("r","receive","pw")
        self.message  = NotifyMessage.add("what",self.sender,self.receiver)

    def test_create_mesage(self):
        eq_(NotifyMessage.objects().count(),1)

    def test_get_notify_message_by_id(self):
        nm  = NotifyMessage.get_notify_message_by_id(self.message.id)
        eq_(nm,self.message)

    def test_get_user_notify_counter(self):
        counter = NotifyMessage.get_user_notify_counter(self.sender)
        eq_(counter,0)
        counter = NotifyMessage.get_user_notify_counter(self.receiver)
        eq_(counter,1)

    def test_get_notify_message_for_user(self):
        nms = NotifyMessage.get_notify_message_for_user(self.sender)
        eq_(len(nms),0)
        nms = NotifyMessage.get_notify_message_for_user(self.receiver)
        eq_(nms[0],self.message)
        
    def test_user_get_notify_messages(self):
        nms = self.receiver.get_notify_messages()
        eq_(nms[0],self.message)

    def test_read(self):
        ok_(not self.message.has_read)
        result = self.message.read(self.receiver)
        ok_(result)
        ok_(self.message.has_read)

    def tearDown(self):
        User.drop_collection()
        NotifyMessage.drop_collection()



class TestPrivateMessage(unittest.TestCase):
    def setUp(self):
        self.sender   = user_create("s","send","pw")
        self.receiver = user_create("r","receive","pw")
        self.message  = PrivateMessage.add("what",self.sender,self.receiver)

    def test_create_mesage(self):
        eq_(PrivateMessage.objects().count(),1)

    def test_get_private_message_by_id(self):
        nm  = PrivateMessage.get_private_message_by_id(self.message.id)
        eq_(nm,self.message)

    def test_get_user_private_message_counter(self):
        counter = PrivateMessage.get_user_private_message_counter(self.sender)
        eq_(counter,0)
        counter = PrivateMessage.get_user_private_message_counter(self.receiver)
        eq_(counter,1)

    def test_get_private_message_for_user(self):
        nms = PrivateMessage.get_private_message_for_user(self.sender)
        eq_(len(nms),0)
        nms = PrivateMessage.get_private_message_for_user(self.receiver)
        eq_(nms[0],self.message)

    def test_read(self):
        ok_(not self.message.has_read)
        result = self.message.read(self.receiver)
        ok_(result)
        ok_(self.message.has_read)
        
    def test_send_private_message(self):
        result = self.sender.send_private_message(self.receiver.id,"123")
        ok_(result)
        eq_(PrivateMessage.objects().count(),2)
        
    def test_user_get_all_private_message(self):
        pms   = self.receiver.get_all_private_message()
        eq_(pms[0],self.message)
    
    def test_user_private_counter(self):
        eq_(self.sender.private_counter,0)
        eq_(self.receiver.private_counter,1)

    def tearDown(self):
        User.drop_collection()
        PrivateMessage.drop_collection()




