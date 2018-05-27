# Generated by Django 2.0.5 on 2018-05-27 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datainput', '0005_auto_20180527_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='familyprofile',
            name='status',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='familyprofileline',
            name='educational_attainment',
            field=models.CharField(choices=[('Elementary Undergraduate', 'Elementary Undergraduate'), ('Elementary Graduate', 'Elementary Graduate'), ('Highschool Undergraduate', 'Highschool Undergraduate'), ('Highschool Graduate', 'Highschool Graduate'), ('College Undergraduate', 'College Undergraduate'), ('College Graduate', 'College Graduate'), ('Vocational', 'Vocational'), ('Others', 'Others')], max_length=50),
        ),
        migrations.AlterField(
            model_name='familyprofileline',
            name='food_production_activity',
            field=models.CharField(choices=[('Vegetable Garden', 'Vegetable Garden'), ('Poultry/Livestock', 'Poultry/Livestock'), ('Fishpond', 'Fishpond')], max_length=10),
        ),
        migrations.AlterField(
            model_name='familyprofileline',
            name='toilet_type',
            field=models.CharField(choices=[('Water Sealed', 'Water Sealed'), ('Open Pit', 'Open Pit'), ('Others', 'Others'), ('None', 'None')], max_length=10),
        ),
        migrations.AlterField(
            model_name='familyprofileline',
            name='water_sources',
            field=models.CharField(choices=[('Pipe', 'Pipe'), ('Well', 'Well'), ('Spring', 'Spring')], max_length=10),
        ),
    ]
