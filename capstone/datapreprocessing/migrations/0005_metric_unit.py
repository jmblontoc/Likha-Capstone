# Generated by Django 2.0.5 on 2018-06-21 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datapreprocessing', '0004_auto_20180617_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='unit',
            field=models.CharField(choices=[('Total', 'Total'), ('Rate', 'Rate')], default='Total', max_length=20),
        ),
    ]
