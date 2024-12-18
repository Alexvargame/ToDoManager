# Generated by Django 5.0.7 on 2024-11-19 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_alter_task_description_alter_task_remark'),
    ]

    operations = [
        migrations.CreateModel(
            name='EveryDayTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.JSONField()),
                ('date_everydaytask', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Каждодневное задание',
                'verbose_name_plural': 'Каждодневные задания',
            },
        ),
    ]
