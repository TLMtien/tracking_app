# Generated by Django 3.2.9 on 2021-12-04 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outlet', '0003_auto_20211204_1636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outletinfo',
            name='outletID',
        ),
    ]
