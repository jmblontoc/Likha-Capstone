# Generated by Django 2.0.5 on 2018-06-19 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datainput', '0013_auto_20180619_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='immunization',
            name='given_bcg',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='immunization',
            name='given_hepa',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='immunization',
            name='given_mcv',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='immunization',
            name='given_opv',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='immunization',
            name='given_pcv',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='immunization',
            name='given_penta',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='immunization',
            name='given_rota',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
