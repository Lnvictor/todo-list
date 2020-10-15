from django.db import models
from django.contrib.auth.models import User

status_choices = [("Done", "Done"), ("Pending", "Pending")]


class Task(models.Model):
    task_name = models.CharField(max_length=30)
    description = models.TextField()
    pub_date = models.DateField("date published", auto_now_add=True)
    status = models.CharField(
        max_length=120, choices=status_choices, default="Pending"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_name

    class Meta:
        ordering = ["-pub_date"]


class Issue(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    issue_description = models.TextField()
    pub_date = models.DateField("date published", auto_now_add=True)
    status = models.CharField(
        max_length=120, choices=status_choices, default="Pending"
    )

    def __str__(self):
        return self.issue_description

    class Meta:
        ordering = ["-pub_date"]
