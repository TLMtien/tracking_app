# Generated by Django 3.2.9 on 2021-12-11 16:26

from django.db import migrations, models
import outlet.models


class Migration(migrations.Migration):

    dependencies = [
        ('outlet', '0003_search'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posmreport',
            name='image',
            field=models.FileField(upload_to=outlet.models.upload_to),
        ),
    ]