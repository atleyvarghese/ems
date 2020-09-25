# coding=utf-8
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from apps.tasks.views import TaskViewSet

router = routers.DefaultRouter()
router.register(r'^tasks', TaskViewSet, basename='manage-tasks')

urlpatterns = [

    path('v1/', include(router.urls)),
    path('v1/token/', obtain_auth_token, name='api_token_auth'),

]
