import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init():
        pass


class ProductionConfig(Config):

    credentials = dict(
        driver          = "mysql+pymysql",  # pilote de la base de données ,  mysql ou bien postgresql
        database_name   = os.environ.get('database_name'),  # Nom de la base de donnée,
        host            = os.environ.get('server'),
        password        = os.environ.get('pwd'),  # mot de passe de la base de données,
        user            = os.environ.get('username'),
        port            = os.environ.get('port')
    )
    SQLALCHEMY_DATABASE_URI = "{driver}://{user}:{password}@{host}:{port}/{database_name}".format(**credentials)
    

class DevelopmentConfig(Config):
    credentials = dict(
        driver="mysql+pymysql",  # pilote de la base de données ,  mysql ou bien postgresql
        database_name="nomadix",  # Nom de la base de donnée,
        host="localhost",
        password="oualid_1992",  # mot de passe de la base de données,
        user="root",
        port=5432
    )
    SQLALCHEMY_DATABASE_URI = "{driver}://{user}:{password}@{host}:{port}/{database_name}".format(**credentials)
    # print(SQLALCHEMY_DATABASE_URI)

class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'FVZBVIjCr_tmGd99dNZEbd9xp9KGe6iuh9U0kBzh6p4oQFSu8jLLe2J3WdfO3HIdnbr1vNhjGcgprT4bJg1kmQ'
    WTF_CSRF_ENABLED=True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///nomadix.sqlite'

configs={
    'dev':DevelopmentConfig,
    'test':TestingConfig,
    'prod':ProductionConfig
}