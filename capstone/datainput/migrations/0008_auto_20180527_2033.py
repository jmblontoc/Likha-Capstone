# Generated by Django 2.0.5 on 2018-05-27 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datainput', '0007_auto_20180527_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familyprofileline',
            name='household_no',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]