# Generated by Django 3.2.9 on 2021-12-07 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outlet', '0008_report_sale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consumerapproachreport',
            name='outlet',
        ),
    ]
