# Generated by Django 3.1.1 on 2024-03-17 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20240316_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentgrade',
            name='teacher_evaluation',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='teachergrade',
            name='student_evaluation',
            field=models.CharField(default='', max_length=150),
        ),
    ]
