from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse


from .forms import SignUpForm
from .facade import user_existis, remove_user
from ..base.views import home


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
            return HttpResponseRedirect("/auth/sign-up-success/")

    else:
        form = SignUpForm()
    return render(
        request,
        "authentication/sign.html",
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
            return HttpResponseRedirect("/auth/login-validation/")
    else:
        form = SignUpForm()

    return render(
        request,
        "authentication/login.html",
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
    return HttpResponseRedirect("/auth/login-failed/")


def set_logout(request: HttpRequest) -> HttpResponseRedirect:
    """
    realizes the logout of plataform

    Args:
        - request (HttpRequest)

    Return: HttpResponseRedirect
    """
    logout(request)
    return HttpResponseRedirect("/auth/login/")
