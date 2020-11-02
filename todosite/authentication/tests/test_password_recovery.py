import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from todosite.assert_contains import assert_contains


@pytest.fixture
def resp(client, db):
    p = client.get(reverse("authentication:passwd-recovery"))
    return p


@pytest.fixture
def change_password_mock(mocker):
    return mocker.patch("todosite.authentication.views.passwd_recovery")


def test_passwd_recovery_status_code(resp):
    assert resp.status_code == 200


def test_change_passwd(client, db, change_password_mock):
    data = client.post(
        reverse("authentication:passwd-recovery"),
        {
            "username": "Testezin",
            "new_password": "testezin@123",
            "confirm_password": "testezin@123",
        },
        secure=True,
    )

    assert data.status_code == 302
