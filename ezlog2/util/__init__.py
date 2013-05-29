# -*- coding: utf-8 -*-

from datetime import datetime as dt
from time import mktime
import random
import re
import bleach

_at_user_re = re.compile(ur"@(\w+) ")


def clean(text):
    return bleach.clean(
        text,
        strip=True)

def linkify(text):
    t_text = text + " "
    t_text = bleach.linkify(t_text)
    t_text = re.sub(r"(@(\w+)) ",r'<a href="/user/nickname/\g<2>">\g<1></a>',t_text)
    return t_text

def find_all_at_users(content):
    tstr    = content + " "
    return set(_at_user_re.findall(tstr))

def sha224(password):
    import hashlib
    return hashlib.sha224(password).hexdigest()

def readable_time(d):
    now = dt.now()
    now_sec = mktime(now.timetuple())
    time_sec = mktime(d.timetuple())
    delta = now_sec - time_sec
    if delta < 60:
        return u"%s秒前" % int(delta)
    elif 60 <= delta < 60*60:
        return u"%s分钟前" % int(delta/60)
    elif 60*60 <= delta < 60*60*24:
        return u"%s小时前" % int(delta/60/60)
    elif 60*60*24 <= delta < 60*60*24*30:
        return u"%s天前" % int(delta/60/60/24)
    elif 60*60*24*30 <= delta < 60*60*24*90:
        return u"%s个月前" % int(delta/60/60/24/30)
    else:
        return d.strftime("%Y年%m月%d日 %H:%M").decode('utf-8')

def random_int():
    return int(random.random()*10000//1)