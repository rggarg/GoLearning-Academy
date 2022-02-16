from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('courses.urls')),
    path('authentication/', include('authentication.urls')),
    path('quiz/', include('quiz.urls')),
    path('teacher/', include('teacher.urls')),


]
