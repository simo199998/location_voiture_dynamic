# Generated by Django 5.0.4 on 2024-05-22 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0010_commande_reservation_client_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande_reservation',
            name='date_encharge',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='commande_reservation',
            name='date_endepot',
            field=models.DateField(blank=True, null=True),
        ),
    ]
