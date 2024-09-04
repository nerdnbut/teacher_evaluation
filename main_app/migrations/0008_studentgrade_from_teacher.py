# Generated by Django 3.1.1 on 2024-03-18 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_teachergrade_from_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentgrade',
            name='from_teacher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main_app.teacher'),
        ),
    ]
