from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class Course(models.Model):
    owner = models.ForeignKey(User, null=False, on_delete=CASCADE)
    name = models.CharField(max_length=50, null=False)
    slug = models.CharField(max_length=50, null=False, unique=True)
    description = models.TextField()
    price = models.IntegerField(null=False)
    discount = models.IntegerField(null=False, default=0)
    active = models.BooleanField(default=False)
    thumbnail = models.CharField(max_length=250, null=False)
    date = models.DateTimeField(auto_now_add=True)
    resource = models.CharField(max_length=250, null=False)
    length = models.IntegerField(null=False)

    def __str__(self):
        return self.name


class CourseProperty(models.Model):
    description = models.CharField(max_length=100, null=False)
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Tag(CourseProperty):
    pass


class Prerequisite(CourseProperty):
    pass


class Learning(CourseProperty):
    pass


class Video(models.Model):
    title = models.CharField(max_length=100, null=False)
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    serial_number = models.IntegerField(null=False)
    video_id = models.CharField(max_length=100, null=False)
    is_preview = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class UserCourse(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(null=False, default=False)

    def __str__(self):
        return f'{self.user.username} - {self.course.name}'


class Payment(models.Model):
    order_id = models.CharField(max_length=60, null=False)
    payment_id = models.CharField(max_length=60)
    user_course = models.ForeignKey(
        UserCourse, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)


class DoubtQuestion(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=CASCADE)
    course = models.ForeignKey(Course, null=False, on_delete=CASCADE)
    question = models.TextField(unique=True)

    def __str__(self):
        return self.question


class DoubtAnswer(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=CASCADE)
    course = models.ForeignKey(Course, null=False, on_delete=CASCADE)
    question = models.ForeignKey(DoubtQuestion, null=False, on_delete=CASCADE)
    answer = models.TextField(unique=True)

    def __str__(self):
        return self.answer


class CourseRequest(models.Model):
    user = models.CharField(max_length=60, null=False)
    course = models.CharField(max_length=60, null=False)
    roll_no = models.IntegerField(null=False)
    email = models.CharField(max_length=60, null=False)
    name = models.CharField(max_length=60, null=False)
    organization = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.user
