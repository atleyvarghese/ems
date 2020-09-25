# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractTracker(models.Model):
    """
    Tracker model to log the timestamp
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Task(AbstractTracker):
    """
    Model to store Employee Task details
    """
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    estimated_time = models.IntegerField(_('Estimated Time(Minutes)'), default=0)
    actual_time = models.IntegerField(_('Actual Time(Minutes)'), default=0)
    review = models.TextField(_('Review'), blank=True)
    is_reviewed = models.BooleanField(_('Reviewed'), default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_tasks', null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='assigned_tasks', null=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='reviewed_tasks', null=True)
    started_on = models.DateTimeField(null=True, blank=True)
    completed_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        ordering = ['-created_at']

    def __str__(self):
        return '{}-{}'.format(self.name, self.assigned_to)
