# Generated by Django 2.1b1 on 2018-07-20 15:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('causalmodel', '0013_auto_20180719_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='rootcause',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
