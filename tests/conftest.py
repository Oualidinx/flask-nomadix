import pytest
from root import create_app, database as db
from root import models
from root import forms
from ..config import configs
@pytest.fixture(scope='session')
def app():
    """Create a test app with a separate test database"""
    app = create_app(configs['test'])
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def db_session(app):
    with app.app_context():
        yield db
        db.session.rollback()