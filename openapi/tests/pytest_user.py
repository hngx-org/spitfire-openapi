import pytest
from openapi import db
from openapi.models.user import User
import bcrypt
from datetime import datetime

def test_set_password():
    user = User(name="TestUser", email="test@example.com", password="test_password")

    user.set_password("new_password")

    assert bcrypt.checkpw("new_password".encode('utf-8'), user.password.encode('utf-8'))

def test_has_subscription_rights():
    current_month = datetime.now().month
    user = User(name="TestUser", email="test@example.com", password="test_password")
    user.subscription_start_date = datetime(datetime.now().year, current_month, 1)

    assert user.has_subscription_rights()

def test_can_use_ai_service():
    user = User(name="TestUser", email="test@example.com", password="test_password")
    user.credit_limit = 10

    assert user.can_use_ai_service(5)


if __name__ == '__main__':
    pytest.main()
