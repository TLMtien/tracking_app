# Generated by Django 3.2.9 on 2021-12-16 18:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('outlet', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_name', models.CharField(max_length=150, unique=True)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('about', models.TextField(blank=True, max_length=500, verbose_name='about')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_salePerson', models.BooleanField(default=False)),
                ('is_HVN', models.BooleanField(default=False)),
                ('is_HVNVip', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SalePerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=200, null=True)),
                ('province', models.CharField(blank=True, max_length=200, null=True)),
                ('joined', models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='outlet.campain')),
                ('outlet', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='outlet.outletinfo')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HVN_vip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=200, null=True)),
                ('joined', models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HVN',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(choices=[('tigerTP', 'TigerTP'), ('tigerFA', 'TigerFA'), ('tigerHZA', 'TigerHZA'), ('strongbow', 'Strongbow Festive'), ('heineken', 'Heineken Festive'), ('bivina', 'Bivina Festive'), ('larue', 'larue Festive')], default='heineken', max_length=200)),
                ('full_name', models.CharField(blank=True, max_length=200, null=True)),
                ('joined', models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
