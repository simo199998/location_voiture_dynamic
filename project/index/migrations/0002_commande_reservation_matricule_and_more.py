# Generated by Django 5.0.4 on 2024-05-19 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande_reservation',
            name='matricule',
            field=models.CharField(default='0000/0/00', max_length=10),
        ),
        migrations.AddField(
            model_name='commande_reservation',
            name='totalprix',
            field=models.CharField(default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='commande_reservation',
            name='disponibilite',
            field=models.CharField(default='NON', max_length=5),
        ),
    ]
