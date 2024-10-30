import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    pass

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
    print(SQLALCHEMY_DATABASE_URI)

class TestingConfig(Config):
    pass

configs={
    'dev':DevelopmentConfig,
    'test':TestingConfig,
    'prod':ProductionConfig
}


