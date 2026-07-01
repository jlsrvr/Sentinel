import pytest
from tests.factories import QueueFactory, CaseFactory, UserFactory

@pytest.fixture(autouse=True)
def set_factory_session(db):
    QueueFactory._meta.sqlalchemy_session = db
    CaseFactory._meta.sqlalchemy_session = db
    UserFactory._meta.sqlalchemy_session = db