# Generated by Django 3.2.2 on 2021-12-23 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0018_coursestatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursestatus',
            name='course_owner',
            field=models.CharField(default=' ', max_length=50),
        ),
    ]