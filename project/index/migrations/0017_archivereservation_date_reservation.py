# Generated by Django 5.0.4 on 2024-05-29 09:42

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0016_archivereservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivereservation',
            name='date_reservation',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
