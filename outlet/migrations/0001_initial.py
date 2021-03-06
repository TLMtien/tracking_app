# Generated by Django 3.2.9 on 2021-12-16 18:46

from django.db import migrations, models
import outlet.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program', models.CharField(choices=[('tigerTP', 'TAB_TGR'), ('tigerFA', 'FES_TGR'), ('tigerHZA', 'HOT_TGR'), ('heineken', 'TAB_HNK'), ('heineken_hnk', 'SPE_HNK'), ('STB', 'FES_SBW'), ('bivina', 'TAB_BVN'), ('Larue', 'TAB_LRE'), ('Larue_SPE', 'SPE_LRE')], max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='consumerApproachReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consumers_approach', models.CharField(max_length=255)),
                ('consumers_brough', models.CharField(max_length=255)),
                ('Total_Consumers', models.CharField(max_length=255)),
                ('created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='giftReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gift1_received', models.CharField(default='0', max_length=255)),
                ('gift2_received', models.CharField(default='0', max_length=255)),
                ('gift3_received', models.CharField(blank=True, default='0', max_length=255)),
                ('gift1_given', models.CharField(blank=True, default='0', max_length=255)),
                ('gift2_given', models.CharField(blank=True, default='0', max_length=255)),
                ('gift3_given', models.CharField(blank=True, default='0', max_length=255)),
                ('gift1_remaining', models.CharField(blank=True, default='0', max_length=50, null=True)),
                ('gift2_remaining', models.CharField(blank=True, default='0', max_length=50, null=True)),
                ('gift3_remaining', models.CharField(blank=True, default='0', max_length=50, null=True)),
                ('created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='outletInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('area', models.CharField(blank=True, max_length=255, null=True)),
                ('outlet_address', models.CharField(max_length=255)),
                ('outlet_Name', models.CharField(max_length=255)),
                ('ouletID', models.CharField(blank=True, default='00', max_length=255, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now=True)),
                ('created_by_HVN', models.BooleanField(blank=True, default=False)),
            ],
        ),
        migrations.CreateModel(
            name='overallReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirm', models.ImageField(upload_to=outlet.models.report)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='posmReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=outlet.models.upload_to)),
                ('created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='report_sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beer_brand', models.CharField(default='0', max_length=255)),
                ('beer_HVN', models.CharField(default='0', max_length=255)),
                ('beer_other', models.CharField(default='0', max_length=255)),
                ('created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='search',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=255)),
                ('district', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='tableReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('other_table', models.CharField(default='0', max_length=255)),
                ('other_beer_table', models.CharField(default='0', max_length=255)),
                ('brand_table', models.CharField(default='0', max_length=255)),
                ('HVN_table', models.CharField(default='0', max_length=255)),
                ('total_table', models.CharField(blank=True, default='0', max_length=255)),
                ('created', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
