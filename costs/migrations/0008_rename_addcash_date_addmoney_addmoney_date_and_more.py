# Generated by Django 4.1.7 on 2023-06-24 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('costs', '0007_addmoney'),
    ]

    operations = [
        migrations.RenameField(
            model_name='addmoney',
            old_name='addcash_date',
            new_name='addmoney_date',
        ),
        migrations.RenameField(
            model_name='addmoney',
            old_name='addcash_name',
            new_name='addmoney_name',
        ),
        migrations.RenameField(
            model_name='addmoney',
            old_name='addcash_sum',
            new_name='addmoney_sum',
        ),
    ]
