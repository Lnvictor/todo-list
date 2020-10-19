from django.contrib.auth.models import User
from django.urls import reverse
from model_mommy import mommy
import pytest


from todosite.assert_contains import assert_contains


@pytest.fixture
def resp(client, db):
    return client.get(reverse("base:home"))


@pytest.fixture
def authenticate(db):
    user = mommy.make(User)
    user.set_password("senha")
    user.save()
    return user


@pytest.fixture
def resp_login(client, authenticate):
    client.force_login(authenticate)
    return client.get(reverse("base:home"))


def test_home_status_code_without_login(resp):
    assert resp.status_code == 302


def test_home(resp_login):
    assert resp_login.status_code == 200


def test_home_content(resp_login):
    assert_contains(resp_login, "Todo App - Toy Application")
