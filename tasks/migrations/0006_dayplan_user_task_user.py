# Generated by Django 4.1.7 on 2023-04-15 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_categorytask_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='dayplan',
            name='user',
            field=models.CharField(default='admin', max_length=100),
        ),
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.CharField(default='admin', max_length=100),
        ),
    ]