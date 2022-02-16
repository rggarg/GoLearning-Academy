from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
# Create your models here.


class CustomUser(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    roll_no = models.IntegerField(null=False, unique=True)
    organization = models.CharField(max_length=250, null=False)
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name
