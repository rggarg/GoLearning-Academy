from django.contrib import admin
from .models import QuizQuestion

# Register your models here.


class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'user', 'course', 'answer']
    list_filter = ['course', 'user']


admin.site.register(QuizQuestion, QuizQuestionAdmin)
