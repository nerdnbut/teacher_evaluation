# Generated by Django 3.1.1 on 2024-03-15 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20240315_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='self',
            field=models.CharField(default='', max_length=150),
        ),
    ]
