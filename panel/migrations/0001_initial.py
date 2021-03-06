# Generated by Django 4.0 on 2022-01-21 13:21

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Swimming pool management system', max_length=255)),
                ('num_of_swimlanes', models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(1)])),
                ('spots_per_swimlane', models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(1)])),
                ('open_time_weekdays', models.TimeField(default=datetime.time(10, 0))),
                ('close_time_weekdays', models.TimeField(default=datetime.time(18, 0))),
                ('open_time_weekends', models.TimeField(default=datetime.time(10, 0))),
                ('close_time_weekends', models.TimeField(default=datetime.time(16, 0))),
                ('price_weekdays_private_clients', models.DecimalField(decimal_places=2, default=6.99, max_digits=6, validators=[django.core.validators.MinValueValidator(0)])),
                ('price_weekends_private_clients', models.DecimalField(decimal_places=2, default=7.59, max_digits=6, validators=[django.core.validators.MinValueValidator(0)])),
                ('price_weekdays_swim_schools', models.DecimalField(decimal_places=2, default=32.99, max_digits=6, validators=[django.core.validators.MinValueValidator(0)])),
                ('price_weekends_swim_schools', models.DecimalField(decimal_places=2, default=35.99, max_digits=6, validators=[django.core.validators.MinValueValidator(0)])),
                ('swim_schools_treshold', models.DecimalField(decimal_places=2, default=0.35, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
            ],
            options={
                'verbose_name': 'Site Configuration',
            },
        ),
    ]
