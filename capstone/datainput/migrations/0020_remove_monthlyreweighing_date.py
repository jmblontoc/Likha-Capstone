# Generated by Django 2.0.5 on 2018-05-31 04:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datainput', '0019_auto_20180531_1251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monthlyreweighing',
            name='date',
        ),
    ]