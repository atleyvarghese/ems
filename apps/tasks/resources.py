from import_export import resources

from apps.tasks.models import Task


class TaskResource(resources.ModelResource):
    class Meta:
        model = Task
