# Generated by Django 3.1.1 on 2024-03-25 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_auto_20240325_0149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.ManyToManyField(default=1, to='main_app.Course'),
        ),
    ]
