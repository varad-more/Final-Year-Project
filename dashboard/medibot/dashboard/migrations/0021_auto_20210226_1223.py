# Generated by Django 3.1.2 on 2021-02-26 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0020_auto_20210212_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='patient_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.patient'),
        ),
    ]
