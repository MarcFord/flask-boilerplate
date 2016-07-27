from pytz import timezone
import os


class BaseConfig(object):
    """
    Base configuration object for flask project
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 't0p_s3cr3t'
    DEBUG = False
    ASSETS_DEBUG = False
    TESTING = False
    BCRYPT_LOG_ROUNDS = 12


    # Debug toolbar
    DEBUG_TB_ENABLED = False
    DEBUG_TB_PROFILER_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    LOCAL_TIMEZONE = timezone('US/Pacific')
    WTF_CSRF_ENABLED = False

    APPLICATION_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data'))
    LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir, 'logs'))
    VIEWS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'views'))
    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data'))
    ALLOWED_EXTENSIONS = set(['csv', 'txt'])

    #Celery Settings
    CELERY_BROKER_URL = 'amqp://guest@{msg_broker}//'.format(
        msg_broker=os.environ.get('MSG_BROKER_HOST') or '127.0.0.1'
    ),
    CELERY_RESULT_BACKEND = 'amqp://guest@{msg_broker}//'.format(
        msg_broker=os.environ.get('MSG_BROKER_HOST') or '127.0.0.1'
    )
    CELERY_IGNORE_RESULT = True

    #Session Settings
    REDIS_STORAGE = {
        'host': os.environ.get('REDIS_HOST') or '127.0.0.1',
        'port': os.environ.get('REDIS_PORT') or 6379,
        'db': 2,
        'charset': 'utf-8'
    }
    SESSION_KEY_PREFIX = 'FLASK_SESSION'

    REDIS_CACHE_CONFIG = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_HOST': os.environ.get('REDIS_HOST') or '127.0.0.1',
        'CACHE_REDIS_PORT': os.environ.get('REDIS_PORT') or 6379,
        'CACHE_REDIS_DB': 3,
    }

    # sqlAlchemy Configs
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_POOL_SIZE = 12
    SQLALCHEMY_POOL_TIMEOUT = 120
    SQLALCHEMY_MAX_OVERFLOW = 10
    SQLALCHEMY_POOL_RECYCLE = 120
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}".format(
        db=os.environ.get('DB_NAME') or 'flask-boilerplate-app',
        user=os.environ.get('DB_USER') or 'root',
        passwd=os.environ.get('DB_PASS')or 'root',
        host=os.environ.get('DB_HOST') or 'localhost',
        port=os.environ.get('DB_PORT') or 3306
    )

    # Flask-Security Settings Details can be found at https://pythonhosted.org/Flask-Security/configuration.html
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'g4hgMQUX#%6Bnv^v'
    SECURITY_EMAIL_SENDER = 'no-reply@flask-boilerplate.org'
    SECURITY_TOKEN_MAX_AGE = 300  # Token has a 5min timeout
    SECURITY_TRACKABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_REGISTERABLE = True
