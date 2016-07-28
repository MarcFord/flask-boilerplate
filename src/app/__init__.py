import os
import redis
import logging
import warnings
from datetime import datetime
from logging import Formatter
from logging.handlers import RotatingFileHandler
# Flask and Flask Extensions Imports
from flask import Flask
from flask_cache import Cache
from flask_celery import Celery
from flask_migrate import Migrate
from flask_session import Session
from flask_admin import Admin
from flask_security import Security
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from flask.exthook import ExtDeprecationWarning
# Project Base Imports
from lib.session import RedisSessionInterface
from lib.ext.admin.data_store import SQLAlchemyUserDatastore
from lib.ext.model.orm.alchemy_base import AlchemyBase
from .handlers import configure_handlers
from .context_processors import configure_context_processors
from .register_views import register_views, register_admin_views
from .config import config


warnings.simplefilter('ignore', ExtDeprecationWarning)

db = AlchemyBase()
migrate = Migrate()
toolbar = DebugToolbarExtension()
session = Session()
session.auto_flush = False
cache = Cache()
celery = Celery()
bcrypt = Bcrypt()
admin = Admin()
security = Security()


class ApplicationFactory(object):
    """
    Application Factory
    """
    @staticmethod
    def create_application(env='development'):
        """
        Create a Configured Flask Application
        :param env:
        :return:
        """
        from ._models import register_models  # This Registers the models with the app to avoid circular imports
        return Application(env).app


class Application(object):
    """
    Flask Application
    """
    def __init__(self, env):
        self.env = env
        self.app = Flask(__name__, static_folder='../static', template_folder='../templates/')
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
        configure_handlers(self.app, db)
        register_views(self.app)
        self.configure_celery()
        register_admin_views(self.app, admin, db)
        configure_context_processors(self.app, admin)

    def register_plugins(self):
        """
        Register Flask Extensions with the application.
        :return: None
        """
        toolbar.init_app(self.app)
        cache.init_app(self.app, config=self.app.config['REDIS_CACHE_CONFIG'])
        bcrypt.init_app(self.app)
        from models.role import Role
        from models.user import User
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        security.init_app(self.app, user_datastore)
        self.app.user_datastore = user_datastore

    def configure_celery(self):
        """
        Configure Celery to use custom Que and Task Router
        :return: None
        """
        from .celery_queu_config import QueueConfig
        queue_config = QueueConfig()
        self.app.config.update(queue_config())
        celery.init_app(self.app)
        celery.conf['BROKER_URL'] = self.app.config['CELERY_BROKER_URL']

    def configure_session(self):
        """
        Configure Application Session Handler
        :return: None
        """
        redis_session_store = self.app.config['REDIS_STORAGE']
        redis_storage = redis.Redis(host=redis_session_store['host'],
                                    port=redis_session_store['port'],
                                    db=redis_session_store['db'],
                                    encoding=redis_session_store['charset'])
        self.app.session_interface = RedisSessionInterface(
            redis=redis_storage,
            prefix=self.app.config['SESSION_KEY_PREFIX']
        )

    def configure_database(self):
        """
        Configure the database with the application
        :return: None
        """
        db.init_app(self.app)
        migrate.init_app(self.app, db)

    def configure_application_logging(self):
        """
        Configure Application Logging
        :return: None
        """
        self.create_logging_directory()

        logger_handler = self.get_log_handler('flask_app', max_bytes=100000, backup_count=1)

        logger_handler.setFormatter(self.get_log_format())

        logger_handler.setLevel(self.get_log_level())
        self.app.logger.addHandler(logger_handler)

    def configure_alchemy_logging(self):
        """
        Configure SQLAlchemy Logging
        :return: None
        """
        self.create_logging_directory()

        handler = self.get_log_handler('alchemy', max_bytes=100000, backup_count=1)

        handler.setFormatter(self.get_log_format())

        handler.setLevel(self.get_log_level())
        logger = logging.getLogger('sqlalchemy')
        logger.addHandler(handler)

    @staticmethod
    def get_log_format():
        """
        Gets the log formatter
        :return: Log Formatter
        :rtype: Formatter
        """
        return Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        )

    def get_log_level(self):
        """
        Get the Log Level based on the application environment
        :return: int
        """
        if self.env == 'development':
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO
        return log_level

    def get_log_handler(self, log_name, max_bytes=100000, backup_count=1):
        """
        Gets the Log handler to be used by application loggers
        :param log_name: Name of the log
        :param max_bytes: Max number of bytes for a log file to be
        :param backup_count: Number of backup log files to keep
        :return: None
        """
        log_file = os.path.join(self.app.config['LOG_PATH'], '{env}_{name}.log'.format(env=self.env, name=log_name))
        return RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)

    def create_logging_directory(self):
        """
        Creates the log directory if it does not already exist
        :return: None
        """
        if not os.path.exists(self.app.config['LOG_PATH']):
            os.makedirs(self.app.config['LOG_PATH'])
