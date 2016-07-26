from .base_config import BaseConfig
import os


class TestingConfig(BaseConfig):
    """
    Testing specific configs
    """
    ENV = 'testing'
    TESTING = True
    TESTSERVER_PORT = 5000

    # sqlAlchemy Configs
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_POOL_SIZE = 12
    SQLALCHEMY_POOL_TIMEOUT = 120
    SQLALCHEMY_MAX_OVERFLOW = 10
    SQLALCHEMY_POOL_RECYCLE = 120
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}".format(
        db='{name}-testing'.format(name=os.environ.get('DB_NAME') or 'flask-boilerplate-app'),
        user=os.environ.get('DB_USER') or 'root',
        passwd=os.environ.get('DB_PASS')or 'root',
        host=os.environ.get('DB_HOST') or 'localhost',
        port=os.environ.get('DB_PORT') or 3306
    )
