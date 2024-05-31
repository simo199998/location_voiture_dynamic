# Generated by Django 5.0.4 on 2024-05-22 14:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0005_remove_voiture_available_voiture_disponibilite'),
        ('index', '0011_alter_commande_reservation_date_encharge_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande_reservation',
            name='image_permit',
            field=models.ImageField(blank=True, default='true', null=True, upload_to='permit/%y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='commande_reservation',
            name='voiture',
            field=models.OneToOneField(blank=True, default=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='administration.voiture'),
        ),
    ]
