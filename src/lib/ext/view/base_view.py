import re
from flask import abort, jsonify, request, flash, url_for, redirect, render_template, g
from flask import current_app as app
from flask.ext.classy import FlaskView, DecoratorCompatibilityError, get_interesting_members
from itsdangerous import Signer


class BaseView(FlaskView):

    @property
    def request(self):
        return request

    @property
    def logger(self):
        return app.logger

    @property
    def config(self):
        return app._get_current_object().config

    @property
    def param_signer(self):
        return Signer(self.config['SECRET_KEY'])

    @classmethod
    def render(cls, template, **kwargs):
        """
        Render's a Template for returning in a view
        :param template: The Template to use
        :param kwargs: Arguments for the template
        :return: Rendered Template
        """
        return render_template(template, **kwargs)

    @classmethod
    def json(cls, *args, **kwargs):
        return jsonify(*args, **kwargs)

    @classmethod
    def url_for(cls, endpoint, **kwargs):
        return url_for(endpoint, **kwargs)

    @classmethod
    def flash_info(cls, message):
        flash(message, 'notice')

    @classmethod
    def flash_success(cls, message):
        flash(message, 'success')

    @classmethod
    def flash_error(cls, message):
        flash(message, 'error')

    @classmethod
    def redirect(cls, endpoint, **kwargs):
        return redirect(cls.url_for(endpoint, **kwargs))

    @classmethod
    def abort(cls, code=404):
        abort(code)
