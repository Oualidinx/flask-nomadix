import pytest
from root import create_app, database as db
from root import models
from root import forms
# from ..config import configs
@pytest.fixture(scope='session')
def app():
    """Create a test app with a separate test database"""
    app = create_app("test")
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
        db.session.rollback()

from root.models import Booking
@pytest.fixture
def sample_booking(db_session):
    """Reusable sample booking object"""
    booking = Booking(
        total_to_pay=1000.0,
        rest_to_pay=1000.0,
        status='pending',
        is_cancelled=False
    )
    db_session.session.add(booking)
    db_session.session.commit()
    return booking