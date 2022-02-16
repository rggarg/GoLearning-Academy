# Generated by Django 3.2.2 on 2021-12-08 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='resource',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='course',
            name='thumbnail',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user_course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.usercourse'),
        ),
    ]
