# Generated by Django 2.1b1 on 2018-07-08 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datapreprocessing', '0006_auto_20180628_0033'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='is_default',
            field=models.BooleanField(default=True),
        ),
    ]
