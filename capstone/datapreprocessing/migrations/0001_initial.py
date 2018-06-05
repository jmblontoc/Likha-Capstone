# Generated by Django 2.0.5 on 2018-06-05 16:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metric', models.CharField(max_length=150)),
                ('threshold', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]
