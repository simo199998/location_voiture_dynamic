from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=20)
    cin = models.CharField(max_length=20)
    naissance = models.DateField()
    permit = models.CharField(max_length=20)
    delevrence = models.DateField()
    email = models.CharField(max_length=30)
    adresse = models.CharField(max_length=50)
    adresse2 = models.CharField(max_length=50, blank=True, null=True)
    pays = CountryField(blank_label='(choisissez un pays)')
    phone = PhoneNumberField(region='MA')
    image_user = models.ImageField(upload_to='user/%y/%m/%d', blank=True, null=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
