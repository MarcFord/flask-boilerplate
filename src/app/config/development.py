from .base_config import BaseConfig


class DevelopmentConfig(BaseConfig):
    """
    Development specific configs
    """
    ENV = 'development'
    DEBUG = True
    ASSETS_DEBUG = True

    # Debug toolbar
    DEBUG_TB_ENABLED = True
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
