from flask import Flask
from flask.templating import render_template
from flask_cache import Cache
from flask_celery import Celery
from flask_migrate import Migrate
from flask_session import Session
from flask_admin import Admin
from lib.ext.model.orm.alchemy_base import AlchemyBase
from lib.session import RedisSessionInterface
from .config import config
from datetime import datetime
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from logging import Formatter
from logging.handlers import RotatingFileHandler
import os
import redis
import logging
import uuid

db = AlchemyBase()
migrate = Migrate()
toolbar = DebugToolbarExtension()
session = Session()
session.auto_flush = False
cache = Cache()
celery = Celery()
bcrypt = Bcrypt()
admin = Admin()


class ApplicationFactory(object):
    @staticmethod
    def create_application(env='development'):
        from ._models import register_models  # This Registers the models with the app to avoid circular imports
        return Application(env).app


class Application(object):

    def __init__(self, env):
        self.env = env
        self.app = Flask(__name__, static_folder='./static', template_folder='./templates/')
        self.config = config[env]
        self.app.config.from_object(self.config)
        self.app.env = self.env
        self.app.debug = self.app.config['DEBUG']
        self.app.secret_key = self.app.config['SECRET_KEY']
        self.app.started_up_at = datetime.utcnow()
        self.configure_application_logging()
        self.configure_alchemy_logging()
        self.configure_database()
        self.configure_session()
        self.register_plugins()
        self.configure_context_processors()
        self.configure_handlers()
        self.register_controllers()
        self.configure_celery()

    def configure_celery(self):
        from .celery_queu_config import QueueConfig
        queue_config = QueueConfig()
        self.app.config.update(queue_config())
        celery.init_app(self.app)
        celery.conf['BROKER_URL'] = self.app.config['CELERY_BROKER_URL']

    def register_controllers(self):
        from views import views
        for view in views:
            if view['route_base']:
                view['class'].register(app=self.app, route_base=view['route_base'])
            else:
                view['class'].register(app=self.app)

    def register_plugins(self):
        toolbar.init_app(self.app)
        cache.init_app(self.app, config=self.app.config['REDIS_CACHE_CONFIG'])
        bcrypt.init_app(self.app)
        admin.init_app(self.app)

    def configure_session(self):
        redis_session_store = self.app.config['REDIS_STORAGE']
        redis_storage = redis.Redis(host=redis_session_store['host'],
                                    port=redis_session_store['port'],
                                    db=redis_session_store['db'],
                                    encoding=redis_session_store['charset'])
        self.app.session_interface = RedisSessionInterface(redis=redis_storage, prefix=self.app.config['SESSION_KEY_PREFIX'])

    def configure_database(self):
        db.init_app(self.app)
        migrate.init_app(self.app, db)

    def configure_application_logging(self):
        if not os.path.exists(self.app.config['LOG_PATH']):
            os.makedirs(self.app.config['LOG_PATH'])
        log_file = os.path.join(self.app.config['LOG_PATH'], '{env}_application.log'.format(env=self.env))

        logger_handler = RotatingFileHandler(log_file, maxBytes=100000, backupCount=1)

        log_formatter = Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        )
        logger_handler.setFormatter(log_formatter)
        if self.env == 'development':
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO

        logger_handler.setLevel(log_level)
        self.app.logger.addHandler(logger_handler)

    def configure_alchemy_logging(self):
        if not os.path.exists(self.app.config['LOG_PATH']):
            os.makedirs(self.app.config['LOG_PATH'])
        log_file = os.path.join(self.app.config['LOG_PATH'], '{env}_alchemy.log'.format(env=self.env))

        handler = RotatingFileHandler(log_file, maxBytes=100000, backupCount=1)

        formatter = Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        )
        handler.setFormatter(formatter)
        if self.env == 'development':
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO

        handler.setLevel(log_level)
        logger = logging.getLogger('sqlalchemy')
        logger.addHandler(handler)

    def configure_handlers(self):
        app = self.app

        @app.errorhandler(500)
        def error(e):
            return render_template('error500.html', error=e), 500

        @app.errorhandler(404)
        def not_found(e):
            return render_template('error.html', error=e), 404

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

    def configure_context_processors(self):
        app = self.app

        @app.context_processor
        def inject_config():
            return dict(flask_config=app.config)
