# Generated by Django 2.0.5 on 2018-06-05 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('datainput', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='operationtimbang',
            name='uploaded_by',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='core.Profile'),
        ),
    ]
