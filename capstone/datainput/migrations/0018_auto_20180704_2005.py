# Generated by Django 2.1b1 on 2018-07-04 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datainput', '0017_remove_familyprofile_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fhsis',
            name='status',
        ),
        migrations.RemoveField(
            model_name='monthlyreweighing',
            name='status',
        ),
        migrations.RemoveField(
            model_name='operationtimbang',
            name='status',
        ),
    ]