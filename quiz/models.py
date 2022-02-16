from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
# Create your models here.


class QuizQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.CharField(max_length=350, null=False)
    option1 = models.CharField(max_length=350, null=False)
    option2 = models.CharField(max_length=350, null=False)
    option3 = models.CharField(max_length=350, null=False)
    option4 = models.CharField(max_length=350, null=False)
    answer = models.CharField(max_length=350, null=False)
    image = models.CharField(max_length=350,)

    def __str__(self):
        return self.question
