# Generated by Django 3.2.5 on 2021-09-22 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistic_app', '0022_alter_project_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='status_style',
            field=models.CharField(choices=[('badge bg-danger', 'Не начат'), ('badge bg-secondary', 'Подготовка'), ('badge bg-primary', 'В работе'), ('badge bg-success', 'Сдан'), ('badge bg-warning text-dark', 'Тех. обслуживание')], default='badge bg-danger', max_length=200, verbose_name='Статус проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('Не начат', 'Не начат'), ('Подготовка', 'Подготовка'), ('В работе', 'В работе'), ('Сдан', 'Сдан'), ('Тех. обслуживание', 'Тех. обслуживание')], default='Не начат', max_length=200, verbose_name='Статус проекта'),
        ),
    ]