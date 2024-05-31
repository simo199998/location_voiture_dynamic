# voitures/models.py

from django.db import models
from django.contrib.auth.models import User

class Voiture(models.Model):
    MODEL_CHOICES = [(str(year), str(year)) for year in range(2010, 2025)]

    TYPE_CARBURANT_CHOICES = [
        ('Essence', 'Essence'),
        ('Diesel', 'Diesel'),
        ('Electrique', 'Électrique'),
        # Ajoutez d'autres types de carburant
    ]

    BOITE_VITESSE_CHOICES = [
        ('Manuelle', 'Manuelle'),
        ('Automatique', 'Automatique'),
        # Ajoutez d'autres types de boites de vitesse
    ]
    STATUT_CHOICES = [
        ('Bon état', 'Bon état'),
        ('Besoin de réparations mineures', 'Besoin de réparations mineures'),
        ('Besoin de réparations majeures', 'Besoin de réparations majeures'),
    ]

    marque = models.CharField(max_length=100, )
    type = models.CharField(max_length=100)
    matricule = models.CharField(max_length=50)
    date_achat = models.DateField()
    image = models.ImageField(upload_to='voitures/')
    puissance_fiscale = models.DecimalField(max_digits=5, decimal_places=2)
    type_carburant = models.CharField(max_length=50, choices=TYPE_CARBURANT_CHOICES)
    boite_vitesse = models.CharField(max_length=50, choices=BOITE_VITESSE_CHOICES)
    model = models.CharField(max_length=100,choices=MODEL_CHOICES)
    montant_achat = models.DecimalField(max_digits=10, decimal_places=2)
    prix=models.CharField(max_length=10, default='0')
    statut_mecanique = models.CharField(max_length=50, choices=STATUT_CHOICES, default='Bon état')
    disponibilite=models.CharField(max_length=5,default='oui')
    def save(self, *args, **kwargs):
        self.disponibilite = self.disponibilite.lower()
        super(Voiture, self).save(*args, **kwargs)
    def __str__(self):
        return self.marque

class Assurance(models.Model):
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    type_assurance = models.CharField(max_length=100)

class VisiteTechnique(models.Model):
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()

class Vignette(models.Model):
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"