# Generated by Django 3.2.5 on 2021-08-24 08:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistic_app', '0012_alter_userlocation_loc_class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstatistic',
            name='pub_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Время события'),
        ),
    ]
