# Generated by Django 2.1b1 on 2018-07-19 02:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('causalmodel', '0011_auto_20180718_0003'),
    ]

    operations = [
        migrations.AddField(
            model_name='causalmodel',
            name='uploaded_by',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='core.Profile'),
        ),
    ]