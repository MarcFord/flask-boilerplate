from flask_admin.contrib.sqla import ModelView
from flask import url_for, redirect, request, abort
from flask_security import current_user
from flask import current_app as app


class AdminView(ModelView):
    @property
    def super_user_role(self):
        return app._get_current_object().config['SUPER_USER_ROLE']

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role(self.super_user_role):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))
