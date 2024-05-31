from typing import Any
from django.db import models
from administration.models import Voiture, Notification
from account.models import Client
from django.utils import timezone
# Create your models here.


class Commande_reservation(models.Model):
    client = models.OneToOneField(Client, on_delete=models.PROTECT)
    voiture = models.OneToOneField(Voiture, on_delete=models.PROTECT, blank=True, null=True)
    image_permit = models.ImageField(upload_to='permit/%y/%m/%d', blank=True, null=True)
    matricule = models.CharField(max_length=10, default='0000/0/00')
    totalprix = models.CharField(max_length=10, default='0')
    date_encharge = models.DateField(null=True, blank=True)
    date_endepot = models.DateField(null=True, blank=True)
    disponibilite = models.CharField(max_length=5, default='NON')
    available=models.BooleanField(default=False)
    def __str__(self):
        return f"Reservation par {self.client}"
    def save(self, *args, **kwargs):
        super(Commande_reservation, self).save(*args, **kwargs)
        if self.available and self.date_endepot:
            ArchiveReservation.objects.create(
                client=self.client,
                voiture=self.voiture,
                image_permit=self.image_permit,
                matricule=self.matricule,
                totalprix=self.totalprix,
                date_encharge=self.date_encharge,
                date_endepot=self.date_endepot,
                disponibilite=self.disponibilite,
                available=self.available
            )
    

class ArchiveReservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    voiture = models.ForeignKey(Voiture, on_delete=models.PROTECT, blank=True, null=True)
    image_permit = models.ImageField(upload_to='permit/%y/%m/%d', blank=True, null=True)
    matricule = models.CharField(max_length=10, default='0000/0/00')
    totalprix = models.IntegerField()
    date_encharge = models.DateField(null=True, blank=True)
    date_endepot = models.DateField(null=True, blank=True)
    disponibilite = models.CharField(max_length=5, default='NON')
    available = models.BooleanField(default=False)
    date_reservation = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"Archive Reservation par {self.client}"