# coding=utf-8
from datetime import datetime, timedelta

from celery import Task as CeleryTask
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from apps.tasks.models import Task
from apps.tasks.resources import TaskResource
from ems.celery import app as celery_app


class WeeklyTaskSheet(CeleryTask):
    """
    Send last weeks Task summary to superuser
    """

    def run(self, **kwargs):
        self.weekly_task_sheet()

    def weekly_task_sheet(self):
        resource = TaskResource()
        recipients = User.objects.filter(is_superuser=True).values_list('email', flat=True)
        # Find the last week start and end date
        last_weekday = datetime.now().date() - timedelta(days=7)
        start_date = last_weekday - timedelta(days=last_weekday.weekday())
        end_date = start_date + timedelta(days=7)
        tasks = Task.objects.filter(created_at__range=[start_date, end_date])
        if tasks.exists() and recipients:
            dataset = resource.export(tasks)
            attachments = []
            attachments.append({'filename': "weekly-task-sheet-{}--{}.xlsx".format(start_date.strftime('%d/%b/%Y'),
                                                                                   end_date.strftime('%d/%b/%Y')),
                                'content': dataset.xlsx,
                                'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                                })
            messages = {}
            messages['subject'] = "Task Sheet for {} - {}".format(start_date.strftime('%d/%b/%Y'),
                                                                  end_date.strftime('%d/%b/%Y'))
            messages['body'] = """Hi,
            Please find the attached Weekly Task Sheet for {} - {}.
            """.format(start_date.strftime('%d/%b/%Y'), end_date.strftime('%d/%b/%Y'))
            self.send_email_messages(recipients, messages, attachments=attachments)

    def send_email_messages(self, recipient, messages, cc=None, attachments=None):
        from_email = settings.DEFAULT_FROM_EMAIL
        email = EmailMessage(messages['subject'],
                             messages['body'],
                             from_email='{} <{}>'.format('EMS', from_email),
                             to=[recipient],
                             cc=cc,
                             )
        if attachments:
            for attachment in attachments:
                email.attach(attachment['filename'], attachment['content'], attachment['mimetype'])

        email.send()

        return email


WeeklyTaskSheet = celery_app.register_task(WeeklyTaskSheet())
