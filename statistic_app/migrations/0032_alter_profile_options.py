# Generated by Django 3.2.5 on 2021-09-27 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistic_app', '0031_profile_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['-user'], 'verbose_name': 'Сотрудник', 'verbose_name_plural': 'Сотрудники'},
        ),
    ]