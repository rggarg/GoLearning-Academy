from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name="dashboard"),
    path('quiz_details', views.quiz_details, name="quiz_details"),
    path('course_details', views.course_details, name="course_details"),
    path('learner_details', views.learner_details, name="learner_details"),
    path('allow_user/<str:id>', views.allow_user, name="allow_user"),
    path('add_video/<str:slug>', views.add_video, name="add_video")
]
