# Generated by Django 4.1.7 on 2023-05-03 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Категория расходов',
                'verbose_name_plural': 'Категории расходов',
            },
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, max_length=30, null=True, verbose_name='Категория')),
                ('cost_date', models.DateField(verbose_name='День')),
                ('cost_name', models.CharField(blank=True, max_length=1000, verbose_name='Назначение')),
                ('cost_sum', models.PositiveIntegerField(verbose_name='Сумма')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cost_created', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Расход',
                'verbose_name_plural': 'Расходы',
            },
        ),
        migrations.CreateModel(
            name='DayCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(default='admin', max_length=100, verbose_name='Пользователь')),
                ('day_date', models.DateField(verbose_name='День')),
                ('costs', models.ManyToManyField(blank=True, related_name='day_costs', to='costs.cost', verbose_name='Расходы')),
            ],
            options={
                'verbose_name': 'Дневной расход',
                'verbose_name_plural': 'Дневные расходы',
            },
        ),
    ]
