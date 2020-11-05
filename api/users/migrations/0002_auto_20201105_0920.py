# Generated by Django 3.1.3 on 2020-11-05 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='social_token',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, max_length=128, verbose_name='Full Name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='Is Staff'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, verbose_name='Is Super User'),
        ),
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('PENDING', 'pending'), ('ACTIVATED', 'activated'), ('BLOCKED', 'blocked')], default='PENDING', max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='verification_code',
            field=models.CharField(blank=True, default=None, max_length=6, null=True, verbose_name='Verification Code'),
        ),
    ]
