from functools import reduce

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from .models import Task, Issue
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.db.utils import IntegrityError
from .forms import SignUpForm, NewTaskForm, NewIssueForm
from .admin import create_task, create_issue, get_task_by_name, user_existis


def home(request: HttpRequest) -> HttpResponse:
    """
    Application homepage view

    Args:
        - request (HttpRequest): Web request for homepage

    Return: (HttpResponse) Web Response that renders the HomePage template
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")

    context = {
        "username": request.user.username,
        "tasks": Task.objects.all(),
        "issues": Issue.objects.all(),
    }
    return render(request, "base/index.html", context)


def get_sign_up(request: HttpRequest, *args: list) -> HttpResponse:
    """
    Sign Up page view, responsible for renders the sign up form

    Args:
        - request (HttpRequest): Web request for the sign uo form page

    Return: (HttpResponse) Web Response that renders the sign up template
    """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/sign-up-success/")

    else:
        form = SignUpForm()
    return render(
        request,
        "base/sign.html",
        {
            "form": form,
            "message": lambda: args[0] if len(args) > 0 else None,
        },
    )


def sign_up_fail(request: HttpRequest) -> HttpResponse:
    """
    render sign up form with an warning message

    Args:
        - request (HttpRequest)

    Return: HttpResponse
    """
    return get_sign_up(request, "Este username já está sendo utilizado")


def sign_sucessfull(request: HttpRequest) -> HttpResponse:
    """
    User's creation view, called after sign up form submission

    Args:
        - request (HttpRequest)

    Return: HttpResponse
    """

    username = request.POST.get("name")
    password = make_password(request.POST.get("passwd"))

    try:
        User.objects.create(username=username, password=password)
        return home(request)
    except IntegrityError:
        return sign_up_fail(request)


def get_login(request: HttpRequest, *args: list) -> HttpResponse:
    """
    Login page view, responsible for renders the login form

    Args:
    - request (HttpRequest): Web request for the login page

    - Optional Arguments:
    - message: message displayed if the previous login failed
    - default value: None

    Return: (HttpResponse) Response that renders the login template
    """
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
            "message": lambda: args[0] if len(args) > 0 else None,
        },
    )


def login_fail(request: HttpRequest) -> HttpResponse:
    """
    calls get_login view with an login failed warning message

    Args:

        - request (HttpRequest)

    Return: HttpResponse
    """
    return get_login(request, "O login falhou, por favor tente novamente")


def validate_login(request: HttpRequest) -> HttpResponseRedirect:
    """
    view responsible for validate the user authentication credentials.

    Args:
        - request (HttpRequest)

    Return: (HttpResponse)
    """
    anonymous_user = authenticate(
        request=request,
        username=request.POST.get("name"),
        password=request.POST.get("passwd"),
    )
    if anonymous_user is not None:
        user = User.objects.filter(password=anonymous_user.password)[0]
        login(request, user)
        return HttpResponseRedirect("/")
    return HttpResponseRedirect("/login-failed")


def set_logout(request: HttpRequest) -> HttpResponseRedirect:
    """
    realizes the logout of plataform

    Args:
        - request (HttpRequest)

    Return: HttpResponseRedirect
    """
    logout(request)
    return HttpResponseRedirect("/login")


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
