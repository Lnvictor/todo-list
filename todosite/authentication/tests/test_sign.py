from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy
import pytest

from todosite.assert_contains import assert_contains


@pytest.fixture
def resp_sign_up(client, db):
    return client.get(reverse("authentication:sign-up"))


@pytest.fixture
def resp_create_user(client, db):
    user = mommy.make(User)
    user.username = "testezin"
    user.set_password("Senha")
    user.save()
    return client.get(reverse("authentication:sign_successfull"))


def test_sign_up(resp_sign_up):
    assert resp_sign_up.status_code == 200


def test_sign_up_content(resp_sign_up):
    assert_contains(resp_sign_up, "Todo App - Cadastrar")


def test_create_user(resp_create_user):
    assert resp_create_user.status_code == 200
