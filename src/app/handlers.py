from flask.templating import render_template
import uuid


def configure_handlers(app, db):
    @app.errorhandler(500)
    def error(e):
        return render_template('errors/500.html', error=e), 500

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html', error=e), 404

    @app.after_request
    def after_request(response):
        if db.session.dirty:
            try:
                app.logger.debug('Committing transaction!')
                db.session.commit()
            except Exception as e:
                app.logger.error(e)
        return response

    @app.before_request
    def before_request():
        from flask import g
        g.request_uuid = uuid.uuid4().hex
