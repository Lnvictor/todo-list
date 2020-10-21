from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render


from .models import Task, Issue
from .forms import SignUpForm, NewTaskForm, NewIssueForm
from .facade import create_task, create_issue, get_task_by_name


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
    Create new task card for user

    Args:
        - request: HttpRequest

    return: HttpResponse
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


def new_issue(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Create a new Issue for some task

    Args:
        - request (HttpRequest)
        - pk (int): Parent task id for the created issue

    return: HttpResponse
    """
    task = Task.objects.filter(pk=pk)[0]
    if request.method == "POST":
        form = NewIssueForm(request.POST)
        description = request.POST.get("description")
        pub_date = request.POST.get("pub_date")
        status = request.POST.get("status")

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
        "pk": task.pk,
    }
    return render(request, "base/new_issue.html", context)


def delete_task(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Remove task

    Args:
        - request (HttpRequest)
        - pk (int): task id

    return HttpResponse
    """
    task = Task.objects.filter(pk=pk).delete()
    return HttpResponseRedirect("/")


def change_status_of_task(request, pk: int) -> HttpResponse:
    """
    Change Task status

    Args:
        - request (HttpRequest)
        - pk (int): task id to be apllied the change

    Return: HttpResponse
    """
    choices = ("Pending", "Done")
    task = Task.objects.filter(pk=pk)[0]
    l = list(map(lambda x: x == task.status, choices))
    task.status = choices[l.index(False)]
    task.save()
    return HttpResponseRedirect("/")


def change_status_of_issue(request: HttpRequest, pk: int) -> HttpResponse:
    choices = ("Pending", "Done")
    issue = Issue.objects.filter(pk=pk)[0]
    l = list(map(lambda x: x == issue.status, choices))
    issue.status = choices[l.index(False)]
    issue.save()
    return HttpResponseRedirect("/")


def delete_issue(request: HttpRequest, pk: int):
    issue = Issue.objects.filter(pk=pk)[0]
    issue.delete()
    return HttpResponseRedirect("/")
