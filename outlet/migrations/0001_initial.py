# Generated by Django 3.2.9 on 2021-12-03 14:46

from django.db import migrations, models
import outlet.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='giftInform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gift1_received', models.IntegerField(default=0)),
                ('gift2_received', models.IntegerField(default=0)),
                ('gift3_received', models.IntegerField(default=0)),
                ('gift1_given', models.IntegerField(default=0)),
                ('gift2_given', models.IntegerField(default=0)),
                ('gift3_given', models.IntegerField(default=0)),
                ('total_survive_gift1', models.CharField(blank=True, max_length=50, null=True)),
                ('total_survive_gift2', models.CharField(blank=True, max_length=50, null=True)),
                ('total_survive_gift3', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='outletInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('province', models.CharField(blank=True, max_length=255, null=True)),
                ('outletID', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('area', models.CharField(blank=True, max_length=255, null=True)),
                ('outlet_address', models.CharField(max_length=255)),
                ('outlet_Name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='posmInform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=outlet.models.upload_to)),
            ],
        ),
        migrations.CreateModel(
            name='reportData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirm', models.ImageField(upload_to=outlet.models.report)),
            ],
        ),
        migrations.CreateModel(
            name='saleInform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_volume_sales', models.IntegerField(default=0)),
                ('brand_table', models.IntegerField(default=0)),
                ('other_HVS_table', models.IntegerField(default=0)),
                ('total_table', models.IntegerField(default=0)),
                ('consumers_approach', models.CharField(max_length=255)),
                ('consumers_brough', models.CharField(max_length=255)),
                ('Total_Consumers', models.CharField(max_length=255)),
            ],
        ),
    ]
