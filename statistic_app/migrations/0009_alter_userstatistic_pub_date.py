# Generated by Django 3.2.5 on 2021-07-22 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistic_app', '0008_alter_userstatistic_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstatistic',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время публикации'),
        ),
    ]