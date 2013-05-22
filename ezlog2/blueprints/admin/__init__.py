from flask.ext.admin import Admin

from .view import ModelView,MyAdminView

from ezlog2.model import User

admin = Admin(name = "Ezlog2 Admin", index_view = MyAdminView(endpoint="admin", url="/admin"))
admin.add_view(ModelView(User))
