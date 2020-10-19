from django.contrib import admin
from django.contrib.auth.models import User
from .models import Task, Issue

# Register your models here.
admin.site.register(Task)
admin.site.register(Issue)
