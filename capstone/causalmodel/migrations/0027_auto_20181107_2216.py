# Generated by Django 2.1b1 on 2018-11-07 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('causalmodel', '0026_suggestedintervention_is_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestedintervention',
            name='metric',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='datapreprocessing.Metric'),
        ),
    ]
