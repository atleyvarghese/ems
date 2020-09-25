# coding=utf-8
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    Model ViewSet to manage Task model
    """
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Update the serializer context with the request object
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Task.objects.all()
        else:
            return Task.objects.filter(Q(assigned_to=self.request.user) | Q(created_by=self.request.user)).distinct()
