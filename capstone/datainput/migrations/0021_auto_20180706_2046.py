# Generated by Django 2.1b1 on 2018-07-06 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datainput', '0020_auto_20180706_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='childcare',
            name='pneumonia_cases',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Pneumonia cases'),
        ),
    ]
