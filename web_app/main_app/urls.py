from django.urls import path

from . import views
from django.conf.urls import url

urlpatterns = [
    path('tracking', views.dashboard, name='tracking-dashboard'),
    path('feedback/', views.feedback, name='app_feedback'),
    path('', views.index, name='app_home'),
]
