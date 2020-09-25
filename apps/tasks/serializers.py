# coding=utf-8
from rest_framework import serializers

from apps.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('name', 'description', 'review', 'is_reviewed', 'estimated_time', 'actual_time',
                  'completed_on')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.context['request'].user.is_superuser:
            # Make the review and is_reviewed fields readonly to user other than superusers
            self.fields['review'].read_only = True
            self.fields['is_reviewed'].read_only = True

    def create(self, validated_data):
        task = super().create(validated_data)

        # Update the created_by and assigned_to with current logged in user
        task.created_by = self.context['request'].user
        task.assigned_to = self.context['request'].user
        task.save()
        return task

    def update(self, instance, validated_data):
        is_reviewed_old_status = instance.is_reviewed
        task = super().update(instance, validated_data)
        if is_reviewed_old_status is False and task.is_reviewed and self.context['request'].user.is_superuser:
            # Update the reviewed_by with current logged in user
            task.reviewed_by = self.context['request'].user
            task.save()
        return task
