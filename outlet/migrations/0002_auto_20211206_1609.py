# Generated by Django 3.2.9 on 2021-12-06 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outlet', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outletinfo',
            name='SP',
        ),
        migrations.AddField(
            model_name='outletinfo',
            name='time',
            field=models.TimeField(auto_now=True),
        ),
    ]
