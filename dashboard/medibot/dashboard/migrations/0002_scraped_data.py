# Generated by Django 3.1 on 2020-08-26 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='scraped_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=500)),
                ('summary', models.CharField(max_length=500)),
                ('links', models.CharField(max_length=500)),
            ],
        ),
    ]
