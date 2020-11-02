from .models import Task, Issue
from django.contrib.auth.models import User


def create_task(
    task_name: str,
    description: str,
    pub_date,
    status: str,
    user: User,
) -> None:

    task = Task(
        task_name=task_name,
        description=description,
        pub_date=pub_date,
        status=status,
        user=user,
    )
    task.save()


def get_task_by_name(task_name: str) -> Task:
    for task in Task.objects.all():
        if task.task_name == task_name:
            return task


def create_issue(issue_description: str, pub_date, status: str, task: Task) -> None:

    issue = Issue(
        task=task,
        issue_description=issue_description,
        pub_date=pub_date,
        status=status,
    )
    issue.save()
