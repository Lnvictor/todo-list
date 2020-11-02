from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from ..base.models import Task, Issue
from .forms import ChangeUserName


@login_required(login_url="../../auth/login/")
def get_profile(request: HttpRequest) -> HttpResponse:
    """
    loads the user profile

    Args:
        - request (HttpRequest)

    return: HttpResponse
    """
    user = request.user
    tasks = Task.objects.filter(user=user)

    buffer = list()
    issues = list(Issue.objects.all())
    issue = list(filter(lambda x: x.task in tasks, issues))

    context = {
        "pk": user.pk,
        "username": user.username,
        "number_tasks": len(tasks),
        "number_issues": len(issue),
    }
    return render(request, "user_profile/profile.html", context)


@login_required
def delete_account(request: HttpRequest, username: str) -> HttpResponse:
    """
    Insert some doc here
    """
    name = User.objects.filter(username=username)
    name[0].delete()
    return HttpResponseRedirect("../../../auth/login/")


def change_username(request: HttpRequest, pk: int) -> HttpResponse:
    """Modify user's 'username"""
    message = None

    if request.method == "POST":
        user = User.objects.filter(pk=pk)[0]
        form = ChangeUserName(request.POST)
        new_name = request.POST.get("new_name")

        if len(list(User.objects.filter(username=new_name))) == 0:
            user.username = new_name
            user.save()
            return HttpResponseRedirect("/../profile/")
        else:
            message = "Este username já está sendo utilizado."

    else:
        form = ChangeUserName()

    context = {
        "pk": request.user.pk,
        "username": request.user.username,
        "form": form,
        "message": message,
    }

    return render(request, "user_profile/change_username.html", context=context)
