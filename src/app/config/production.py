from .base_config import BaseConfig
import os


class ProductionConfig(BaseConfig):
    """
    Production specific configs
    """
    ENV = 'production'
    SECRET_KEY = os.environ.get('SECRET_KEY')
