# -*- coding: utf-8 -*-

from datetime import datetime as dt
from time import mktime
import random

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