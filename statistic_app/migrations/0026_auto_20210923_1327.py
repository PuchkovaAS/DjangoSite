# Generated by Django 3.2.5 on 2021-09-23 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('statistic_app', '0025_auto_20210923_1119'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historyproject',
            options={'ordering': ['-pub_date', '-id'], 'verbose_name': 'История проекта', 'verbose_name_plural': 'Истории проекта'},
        ),
        migrations.AlterModelOptions(
            name='userstatistic',
            options={'ordering': ['-pub_date', '-id'], 'verbose_name': 'Статистика пользователя', 'verbose_name_plural': 'Статистика пользователей'},
        ),
        migrations.AddField(
            model_name='userstatistic',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='statistic_app.project', verbose_name='Проект'),
        ),
    ]
