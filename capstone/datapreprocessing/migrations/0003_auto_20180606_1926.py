# Generated by Django 2.0.5 on 2018-06-06 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapreprocessing', '0002_datamap_is_completed'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DataMap',
            new_name='Metric',
        ),
    ]