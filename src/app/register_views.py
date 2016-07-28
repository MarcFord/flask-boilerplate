from views import views
from lib.ext.admin.admin_view import AdminView


def register_views(app):

    for view in views:
        if view['route_base']:
            view['class'].register(app=app, route_base=view['route_base'])
        else:
            view['class'].register(app=app)


def register_admin_views(app, admin, db):
    from models.role import Role
    from models.user import User
    admin.template_mode = 'bootstrap3'
    admin.base_template = 'layouts/admin.html'
    session = db.session
    admin.add_view(AdminView(User, session))
    admin.add_view(AdminView(Role, session))
    admin.init_app(app)
