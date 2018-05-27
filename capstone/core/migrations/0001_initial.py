# Generated by Django 2.0.5 on 2018-05-27 09:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('datainput', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('Barangay Nutrition Scholar', 'Barangay Nutrition Scholar'), ('Nutritionist', 'Nutritionist'), ('Nutrition Program Coordinator', 'Nutrition Program Coordinator')], max_length=40)),
                ('barangay', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='datainput.Barangay')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
