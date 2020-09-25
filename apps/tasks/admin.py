# coding=utf-8
from django.contrib import admin

from apps.tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'assigned_to', 'created_at', 'estimated_time', 'is_reviewed', 'completed_on')


admin.site.register(Task, TaskAdmin)
