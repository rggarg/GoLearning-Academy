from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('add_question/<str:slug>', views.add_question, name='add_question'),
    path('take_quiz/<str:slug>', views.take_quiz, name='take_quiz')
]
