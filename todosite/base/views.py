from functools import reduce

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from .models import Task, Issue
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .forms import SignUpForm, NewTaskForm, NewIssueForm
from .facade import create_task, create_issue, get_task_by_name
from django.contrib.auth.decorators import login_required


@login_required(login_url="/auth/login/")
def home(request: HttpRequest) -> HttpResponse:
    """
    Application homepage view

    Args:
        - request (HttpRequest): Web request for homepage

    Return: (HttpResponse) Web Response that renders the HomePage template
    """
    context = {
        "username": request.user.username,
        "tasks": Task.objects.all(),
        "issues": Issue.objects.all(),
    }
    return render(request, "base/index.html", context)


def new_task(request: HttpRequest) -> HttpResponse:
    """
    Insert some docstr here
    """
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        task_name = request.POST.get("task_name")
        description = request.POST.get("description")
        pub_date = request.POST.get("pub_date")
        status = request.POST.get("status")
        user = request.user
        create_task(
            task_name=task_name,
            description=description,
            pub_date=pub_date,
            status=status,
            user=user,
        )
        return HttpResponseRedirect("/")
    else:
        form = NewTaskForm()

    context = {
        "username": request.user.username,
        "tasks": Task.objects.all(),
        "issues": Issue.objects.all(),
        "form": form,
    }
    return render(request, "base/new_task.html", context)


def new_issue(request: HttpRequest, task_name: str) -> HttpResponse:
    """
    Insert some docstr here

    """
    if request.method == "POST":
        form = NewIssueForm(request.POST)
        description = request.POST.get("description")
        pub_date = request.POST.get("pub_date")
        status = request.POST.get("status")
        task = get_task_by_name(task_name)

        if task is not None:
            create_issue(
                issue_description=description,
                pub_date=pub_date,
                status=status,
                task=task,
            )
        return HttpResponseRedirect("/")
    else:
        form = NewIssueForm()

    context = {
        "username": request.user.username,
        "tasks": Task.objects.all(),
        "issues": Issue.objects.all(),
        "form": form,
        "name": task_name,
    }
    return render(request, "base/new_issue.html", context)


def remove_task(request: HttpRequest, name: str) -> HttpResponse:
    task = Task.objects.filter(task_name=name).delete()
    return HttpResponseRedirect("/")


def change_status_of_task(request, name: str) -> HttpResponse:
    """
    Change Task status

    Args:
        - request (HttpRequest)
        - task_name (str): task name to be apllied the change

    Return: HttpResponse
    """
    choices = ("Pending", "Done")
    task = Task.objects.filter(task_name=name)[0]
    l = list(map(lambda x: x == task.status, choices))
    task.status = choices[l.index(False)]
    task.save()
    return HttpResponseRedirect("/")


def delete_user(request):
    ...
