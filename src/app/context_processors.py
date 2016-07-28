from flask import url_for


def configure_context_processors(app, admin):

    @app.context_processor
    def inject_config():
        return dict(flask_config=app.config)

    @app.context_processor
    def inject_jquery_version():
        return dict(JQUERY_VERSION=app.config['JQUERY_VERSION'])

    @app.context_processor
    def inject_google_analytics():
        return dict(GOOGLE_ANALYTICS_SITE_ID=app.config['GOOGLE_ANALYTICS_SITE_ID'])

    @app.context_processor
    def inject_admin_base():
        from flask_admin import helpers as admin_helpers
        return dict(
            admin_base_template='admin/base.html',
            admin_view=admin.index_view,
            get_url=url_for,
            h=admin_helpers
        )
