# Generated by Django 3.2.5 on 2021-09-21 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistic_app', '0017_agentproject_historyproject_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Название'),
        ),
    ]
