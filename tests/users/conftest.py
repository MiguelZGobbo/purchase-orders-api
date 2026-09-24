import pytest

from db import db
from users.model import UserModel


@pytest.fixture(autouse=True)
def clear_users(test_client):
    with test_client.application.app_context():
        db.session.query(UserModel).delete()
        db.session.commit()
        db.session.remove()
