# Generated by Django 5.0.4 on 2024-05-25 07:52

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_client_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='MA'),
        ),
    ]
