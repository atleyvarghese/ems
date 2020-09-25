# coding=utf-8
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    Model ViewSet to manage Task model
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Update the serializer context with the request object
        context.update({"request": self.request})
        return context
