from functools import reduce

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Task, Issue
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .forms import SignUpForm, NewTaskForm, NewIssueForm
from .admin import create_task, create_issue, get_task_by_name


def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")

    context = {
        "username": request.user.username,
        "tasks": Task.objects.all(),
        "issues": Issue.objects.all(),
    }
    return render(request, "base/index.html", context)


def get_sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.isValid():
            return HttpResponseRedirect("/sign-up-success/")
    else:
        form = SignUpForm()
    return render(request, "base/sign.html", {"form": form})


def get_login(request, *args):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.isValid():
            return HttpResponseRedirect("/login-validation/")
    else:
        form = SignUpForm()

    return render(
        request,
        "base/login.html",
        {
            "form": form,
            "message": args[0],
        },
    )


def login_fail(request):
    return get_login(request, "O login falhou, por favor tente novamente")


def sign_sucefull(request):
    username = request.POST.get("name")
    passwd = make_password(request.POST.get("passwd"))

    User.objects.create(username=username, password=passwd)
    return home(request)


def validate_login(request):
    anonymous_user = authenticate(
        request=request,
        username=request.POST.get("name"),
        password=request.POST.get("passwd"),
    )
    if anonymous_user is not None:
        user = User.objects.filter(password=anonymous_user.password)[0]
        login(request, user)
        return HttpResponseRedirect("/")
    return HttpResponseRedirect("/login-failed/")


def set_logout(request):
    logout(request)
    return HttpResponseRedirect("/login")


def new_task(request):
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


def new_issue(request, name):
    if request.method == "POST":
        form = NewIssueForm(request.POST)
        description = request.POST.get("description")
        pub_date = request.POST.get("pub_date")
        status = request.POST.get("status")
        task = get_task_by_name(name)

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
        "name": name,
    }
    return render(request, "base/new_issue.html", context)


def remove_task(request, name: str) -> None:
    task = Task.objects.filter(task_name=name).delete()
    return HttpResponseRedirect("/")


def change_status_of_task(request, name: str) -> None:
    choices = ("Pending", "Done")
    task = Task.objects.filter(task_name=name)[0]
    l = list(map(lambda x: x == task.status, choices))
    task.status = choices[l.index(False)]
    task.save()
    return HttpResponseRedirect("/")
