# Generated by Django 3.2.5 on 2021-09-21 12:23

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('statistic_app', '0016_remove_profile_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('status', models.CharField(choices=[('Не начат', 'Не начат'), ('Подготовка', 'Подготовка'), ('В работе', 'В работе'), ('Сдан', 'Сдан'), ('Тех. обслуживание', 'Тех. обслуживание')], default='Не начат', max_length=200, verbose_name='Статус проекта')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание события')),
                ('tasks', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Задачи')),
                ('url', models.SlugField(blank=True, default=None, max_length=255, null=True, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекты',
            },
        ),
        migrations.CreateModel(
            name='HistoryProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateField(default=datetime.date.today, verbose_name='Время события')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='statistic_app.project', verbose_name='Проект')),
            ],
            options={
                'verbose_name': 'История проекта',
                'verbose_name_plural': 'Истории проекта',
            },
        ),
        migrations.CreateModel(
            name='AgentProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200, verbose_name='Имя')),
                ('second_name', models.CharField(max_length=200, verbose_name='Фамилия')),
                ('father_name', models.CharField(max_length=200, verbose_name='Отчество')),
                ('position', models.CharField(max_length=200, verbose_name='Должность')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('phone_number', models.CharField(blank=True, max_length=200, null=True)),
                ('url', models.SlugField(blank=True, default=None, max_length=255, null=True, unique=True, verbose_name='URL')),
                ('location', models.ManyToManyField(blank=True, related_name='объекты', to='statistic_app.Project')),
            ],
            options={
                'verbose_name': 'Инагент',
                'verbose_name_plural': 'Инагенты',
            },
        ),
    ]
