from app import ApplicationFactory
from lib.ext.model.orm import db
import pytest
from sqlalchemy_utils import database_exists, drop_database, create_database


@pytest.fixture(autouse=True, scope='module')
def app(request):
    test_app = ApplicationFactory.create_application('testing')
    test_app.app_context().push()
    if database_exists(db.engine.url):
        drop_database(db.engine.url)
    create_database(db.engine.url)
    db.create_all()

    def teardown():
        db.session.expunge_all()
        db.session.remove()
        drop_database(db.engine.url)
        db.engine.dispose()

    request.addfinalizer(teardown)
    return test_app


@pytest.fixture(scope='module')
def app_db():
    return db
