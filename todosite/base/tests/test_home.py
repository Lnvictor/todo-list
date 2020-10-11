from django.test import TestCase
from django.urls import reverse
import pytest

# Create your tests here.


@pytest.fixture
def resp(client, db):
    resp = client.get(reverse("base:home"))
    return resp


def test_home_status_code(resp):
    assert resp.status_code == 200


def test_home_content(resp):
    test = TestCase()
    test.assertContains(resp, "Prévia")
