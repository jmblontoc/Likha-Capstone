# Generated by Django 2.1b1 on 2018-10-22 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datapreprocessing', '0009_metric_json_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='suggested_interventions',
            field=models.TextField(default=''),
        ),
    ]
