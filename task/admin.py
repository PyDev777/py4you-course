from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_filter = ['start_time', 'end_time']
    list_display = ['task', 'start_time', 'end_time', 'status']


# Register your models here.
admin.site.register(Task, TaskAdmin)
