from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='app_home'),
    path('feedback/', views.feedback, name='app_feedback'),
    path('test/', views.test, name='app_test'),

]
