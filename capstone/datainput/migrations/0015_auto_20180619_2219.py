# Generated by Django 2.0.5 on 2018-06-19 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datainput', '0014_auto_20180619_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='immunization',
            name='given_bcg',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='immunization',
            name='given_hepa',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='immunization',
            name='given_mcv',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='immunization',
            name='given_opv',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='immunization',
            name='given_pcv',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='immunization',
            name='given_penta',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='immunization',
            name='given_rota',
            field=models.IntegerField(),
        ),
    ]