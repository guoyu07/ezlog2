from ezlog2.model import User,Tweet
from ezlog2.util import sha224


def user_create(email,nickname,pw):
    return User(email=email,
               nickname=nickname,
               password=sha224(pw)).save()
               

def tweet_create(content):
    return Tweet(content=content).save()