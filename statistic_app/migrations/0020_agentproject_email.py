# Generated by Django 3.2.5 on 2021-09-22 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistic_app', '0019_rename_second_name_agentproject_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentproject',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
