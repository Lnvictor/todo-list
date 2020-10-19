from django.urls import reverse
from model_mommy import mommy
import pytest

from ..models import Task, Issue


@pytest.fixture
def resp_new_task(db):
    task = mommy.make(Task)
    task.task_name = "Task Mommy"
    task.description = "Task Mommy description"
    task.status = "Pending"
    task.save()
    return task


@pytest.fixture
def resp_new_issue(db):
    issue = mommy.make(Issue)
    issue.issue_description = "Test issue description"
    issue.status = "Pending"
    issue.save()
    return issue


def test_new_task(resp_new_task):
    assert resp_new_task in list(Task.objects.all())


def test_new_issue(resp_new_issue):
    assert resp_new_issue in list(Issue.objects.all())
