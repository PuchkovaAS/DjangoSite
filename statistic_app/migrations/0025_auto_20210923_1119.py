# Generated by Django 3.2.5 on 2021-09-23 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('statistic_app', '0024_remove_project_status_style'),
    ]

    operations = [
        migrations.AddField(
            model_name='historyproject',
            name='user_add',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='statistic_app.profile', verbose_name='Сотрудник'),
        ),
        migrations.AlterField(
            model_name='agentproject',
            name='location',
            field=models.ManyToManyField(blank=True, related_name='agents', to='statistic_app.Project', verbose_name='Объект'),
        ),
        migrations.AlterField(
            model_name='historyproject',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='history', to='statistic_app.project', verbose_name='Проект'),
        ),
    ]
