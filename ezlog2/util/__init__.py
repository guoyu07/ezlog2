# -*- coding: utf-8 -*-


def sha224(password):
    import hashlib
    return hashlib.sha224(password).hexdigest()



