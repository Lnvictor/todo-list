from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from ..base.models import Task, Issue


@login_required(login_url="../../auth/login/")
def get_profile(request: HttpRequest) -> HttpResponse:
    user = request.user
    tasks = Task.objects.filter(user=user)

    buffer = list()
    issues = list(Issue.objects.all())
    issue = list(filter(lambda x: x.task in tasks, issues))

    context = {
        "username": user.username,
        "number_tasks": len(tasks),
        "number_issues": len(issue),
    }
    return render(request, "user_profile/profile.html", context)


@login_required
def delete_account(request: HttpRequest, username: str) -> HttpResponse:
    name = User.objects.filter(username=username)
    name[0].delete()
    return HttpResponseRedirect("../../../auth/login/")
