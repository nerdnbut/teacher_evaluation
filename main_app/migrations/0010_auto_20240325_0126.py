# Generated by Django 3.1.1 on 2024-03-24 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_auto_20240318_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='course',
        ),
        migrations.AddField(
            model_name='student',
            name='course',
            field=models.ManyToManyField(null=True, to='main_app.Course'),
        ),
    ]
