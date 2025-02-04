# Generated by Django 5.0.4 on 2024-05-20 22:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0007_remove_commande_reservation_client_delete_client'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=20)),
                ('prenom', models.CharField(max_length=20)),
                ('cin', models.CharField(max_length=20)),
                ('naissance', models.DateField()),
                ('permit', models.CharField(max_length=20)),
                ('delevrence', models.DateField()),
                ('email', models.CharField(max_length=30)),
                ('adresse', models.CharField(max_length=50)),
                ('adresse2', models.CharField(blank=True, max_length=50, null=True)),
                ('pays', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=20)),
                ('image_user', models.ImageField(blank=True, null=True, upload_to='user/%y/%m/%d')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='client_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
