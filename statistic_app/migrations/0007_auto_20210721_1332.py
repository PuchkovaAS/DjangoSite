# Generated by Django 3.2.5 on 2021-07-21 10:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistic_app', '0006_auto_20210721_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 21, 13, 32, 50, 209681), verbose_name='Время изменения'),
        ),
        migrations.AlterField(
            model_name='userstatistic',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 21, 13, 32, 50, 210681), verbose_name='Время публикации'),
        ),
    ]
