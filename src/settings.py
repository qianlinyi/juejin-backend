import os


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_string')
    # 禁止转译中文
    JSON_AS_ASCII = False
    # 数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    USERNAME = os.getenv('DATABASE_USERNAME')
    PASSWORD = os.getenv('DATABASE_PASSWORD')
    HOST = os.getenv('DATABASE_HOST')
    PORT = os.getenv('DATABASE_PORT')
    NAME = os.getenv('DATABASE_NAME')


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        BaseConfig.USERNAME, BaseConfig.PASSWORD, BaseConfig.HOST, BaseConfig.PORT, BaseConfig.NAME
    )


class TestingConfig(DevelopmentConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
