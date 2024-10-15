# Generated by Django 4.1.7 on 2023-05-03 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cost',
            name='category',
        ),
        migrations.AddField(
            model_name='cost',
            name='category',
            field=models.ManyToManyField(related_name='category_cost', to='costs.categorycost', verbose_name='Категория'),
        ),
    ]