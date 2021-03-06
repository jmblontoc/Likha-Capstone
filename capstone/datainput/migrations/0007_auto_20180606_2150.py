# Generated by Django 2.0.5 on 2018-06-06 13:50

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('datainput', '0006_auto_20180606_2056'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChildCare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('given_complimentary_food', models.DecimalField(decimal_places=2, max_digits=5)),
                ('received_vitamin_A', models.DecimalField(decimal_places=2, max_digits=5)),
                ('received_iron', models.DecimalField(decimal_places=2, max_digits=5)),
                ('received_MNP', models.DecimalField(decimal_places=2, max_digits=5)),
                ('sick_children', models.DecimalField(decimal_places=2, max_digits=5)),
                ('given_deworming', models.DecimalField(decimal_places=2, max_digits=5)),
                ('anemic_children', models.DecimalField(decimal_places=2, max_digits=5)),
                ('anemic_children_with_iron', models.DecimalField(decimal_places=2, max_digits=5)),
                ('diarrhea_cases', models.DecimalField(decimal_places=2, max_digits=5)),
                ('diarrhea_with_ORS', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pneumonia_cases', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pneumonia_cases_with_Tx', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='FHSIS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('status', models.CharField(max_length=30)),
                ('barangay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datainput.Barangay')),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Flariasis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cases', models.DecimalField(decimal_places=2, max_digits=5)),
                ('mfd', models.DecimalField(decimal_places=2, max_digits=5)),
                ('given_MDA', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fhsis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datainput.FHSIS')),
                ('sex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datainput.Sex')),
            ],
        ),
        migrations.CreateModel(
            name='Immunization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('immunization_given', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fully_immunized_child', models.DecimalField(decimal_places=2, max_digits=5)),
                ('child_protected_at_birth', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fhsis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datainput.FHSIS')),
                ('sex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datainput.Sex')),
            ],
        ),
        migrations.CreateModel(
            name='Leprosy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cases', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cases_cured', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fhsis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datainput.FHSIS')),
                ('sex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datainput.Sex')),
            ],
        ),
        migrations.CreateModel(
            name='Malaria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('population_at_risk', models.DecimalField(decimal_places=2, max_digits=5)),
                ('malaria_cases', models.DecimalField(decimal_places=2, max_digits=5)),
                ('deaths', models.DecimalField(decimal_places=2, max_digits=5)),
                ('immunization_given', models.DecimalField(decimal_places=2, max_digits=5)),
                ('llin_given', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fhsis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datainput.FHSIS')),
                ('sex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datainput.Sex')),
            ],
        ),
        migrations.CreateModel(
            name='MaternalCare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prenatal_visits', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Pregnant women with 4 or more prenatal visits')),
                ('tetanus_toxoid', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Pregnant women given 2 doses of Tetanus Toxoid')),
                ('tt2_plus', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Pregnant women given TT2 plus')),
                ('complete_iron', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Pregnant women given complete iron with folic acid supplementation')),
                ('complete_iron_post', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Postpartum women with given complete iron supplementation')),
                ('postpartum_visits', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Postpartum women with at least 2 postpartum visits')),
                ('vitamin_a', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Postpartum women given Vitamin A supplementation')),
                ('breastfed', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Postpartum women initiated breastfeeding within 1 hour after delivery')),
                ('deliveries', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fhsis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datainput.FHSIS')),
            ],
        ),
        migrations.CreateModel(
            name='Schistosomiasis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cases_cured', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cases', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fhsis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datainput.FHSIS')),
                ('sex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datainput.Sex')),
            ],
        ),
        migrations.CreateModel(
            name='STISurveillance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_pregnant_women_seen', models.DecimalField(decimal_places=2, max_digits=5)),
                ('number_of_pregnant_women_with_Syphilis', models.DecimalField(decimal_places=2, max_digits=5)),
                ('number_of_pregnant_women_given_Penicillin', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fhsis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datainput.FHSIS')),
            ],
        ),
        migrations.CreateModel(
            name='Tuberculosis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('underwent_ddsm', models.DecimalField(decimal_places=2, max_digits=5)),
                ('smear_positive', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cases_cured', models.DecimalField(decimal_places=2, max_digits=5)),
                ('identified', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fhsis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datainput.FHSIS')),
                ('sex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datainput.Sex')),
            ],
        ),
        migrations.AddField(
            model_name='childcare',
            name='fhsis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datainput.FHSIS'),
        ),
        migrations.AddField(
            model_name='childcare',
            name='sex',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datainput.Sex'),
        ),
    ]
