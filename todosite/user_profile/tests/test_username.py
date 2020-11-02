import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from todosite.base.tests.test_home import resp_login
from todosite.assert_contains import assert_contains


@pytest.fixture
def get_profile(resp_login):
    resp = client.get(reverse("user_profile:passwd-recovery"))
    return resp


def test_username_in_profile(client, get_profile):
    # TODO: Escrever teste para a lógica de troca de username
    ...


#    assert_constains(client.user.username, get_profile)
