from os import name
from django.contrib import admin
from django.urls import path, include
from courses.views import home, coursePage, checkout, my_courses, add_course, get_answers
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home, name='home'),
    path('my_courses', my_courses, name='my_courses'),
    path('checkout/<str:slug>', checkout, name='checkout'),
    path('course/<str:slug>', coursePage, name='coursepage'),
    # path('verify_payment', verifyPayment, name='verify_payment'),
    path('add_course', add_course, name='add_course'),
    path('get_answer/<str:id>', get_answers, name="get_answer")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
