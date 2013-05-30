from flask.ext.admin import Admin
from flask.ext.admin.contrib.mongoengine import ModelView

from .view import UserModelView,MyAdminView,MyModelView,TweetModelView
from ezlog2.model import User,Tweet,Comment
from ezlog2.model.search import SearchIndex

admin = Admin(name = "Flask Microlog Admin", index_view = MyAdminView(endpoint="admin", url="/admin"))
admin.add_view(UserModelView(User))
admin.add_view(TweetModelView(Tweet))
admin.add_view(MyModelView(Comment))
admin.add_view(MyModelView(SearchIndex))