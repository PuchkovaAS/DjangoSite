# Generated by Django 3.2.5 on 2021-09-27 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistic_app', '0033_alter_profile_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agentproject',
            options={'ordering': ['-last_name', '-first_name', '-father_name'], 'verbose_name': 'Контрагент', 'verbose_name_plural': 'Контрагенты'},
        ),
    ]
