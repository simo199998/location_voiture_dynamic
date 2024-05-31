# voitures/forms.py

from django import forms
from .models import Voiture, Assurance, VisiteTechnique, Vignette
from index.models import Commande_reservation
from account.models import Client
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhonePrefixSelect
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class VoitureForm(forms.ModelForm):
    class Meta:
        model = Voiture
        fields = ['marque', 'type', 'matricule', 'date_achat', 'image', 'puissance_fiscale', 'type_carburant', 'boite_vitesse', 'model' ,'montant_achat','prix','statut_mecanique']
        labels = {
            'marque': 'Marque',
            'type': 'Type',
            'matricule': 'Matricule',
            'date_achat': 'Date d\'achat',
            'image': 'Image du voiture',
            'puissance_fiscale': 'Puissance fiscale',
            'type_carburant': 'Type de carburant',
            'boite_vitesse': 'Boîte de vitesse',
            'model': 'Modèle',
            'montant_achat': 'Montant d\'achat',
            'prix': 'Prix/jour',
        }
        widgets = {
            'date_achat': forms.DateInput(attrs={'type': 'date'}),
        }
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['statut_mecanique'].widget = forms.Select(choices=Voiture.STATUT_CHOICES)

    MODEL_CHOICES = Voiture.MODEL_CHOICES
    TYPE_CARBURANT_CHOICES = Voiture.TYPE_CARBURANT_CHOICES
    BOITE_VITESSE_CHOICES = Voiture.BOITE_VITESSE_CHOICES

    type_carburant = forms.ChoiceField(choices=TYPE_CARBURANT_CHOICES)
    boite_vitesse = forms.ChoiceField(choices=BOITE_VITESSE_CHOICES)
    model = forms.ChoiceField(choices=MODEL_CHOICES)


class AssuranceForm(forms.ModelForm):
    class Meta:
        model = Assurance
        fields = ['date_debut', 'date_fin', 'type_assurance']
        labels = {
            'date_debut': 'Date de début assurance',
            'date_fin': 'Date de fine assurance',
            'type_assurance': 'Type d\'assurance',
        }
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        } 
class VisiteTechniqueForm(forms.ModelForm):
    class Meta:
        model = VisiteTechnique
        fields = ['date_debut', 'date_fin']
        labels = {
            'date_debut': 'Date de début la viste',
            'date_fin': 'Date de fine la visite',
        }
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }
    

class VignetteForm(forms.ModelForm):
    class Meta:
        model = Vignette
        fields = ['date_debut', 'date_fin']
        labels = {
            'date_debut': 'Date de début vignette',
            'date_fin': 'Date de fine la vignette',
        }
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }

class CommandeReservationForm(forms.ModelForm):
    class Meta:
        model = Commande_reservation
        fields = '__all__'
    

class UpdateDateForm(forms.ModelForm):
    class Meta:
        model = Commande_reservation
        fields = ['date_encharge', 'date_endepot']


class AdminLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150, 
        required=True,
        
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'cin', 'naissance', 'permit', 'delevrence', 'email', 'adresse', 'adresse2', 'pays', 'phone', 'image_user']

        widgets = {
            'nom': forms.TextInput(attrs={'class':'form-control'}),
            'prenom': forms.TextInput(attrs={'class':'form-control'}),
            'cin': forms.TextInput(attrs={'class':'form-control'}),
            'permit': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'adresse': forms.TextInput(attrs={'class':'form-control'}),
            'adresse2': forms.TextInput(attrs={'class':'form-control'}),
            'naissance': forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'delevrence': forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'phone':PhoneNumberPrefixWidget(initial='MA', attrs={'class': 'form-control d-inline-block w-auto'}),
            'pays':CountrySelectWidget(attrs={'class': 'form-control'}),
            'image_user': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels={
            'nom':' Nom:',
            'prenom': 'Prénom:',
            'cin': 'Numéro CIN:',
            'naissance': 'Date de naissance:',
            'permit': 'Numéro de permis:',
            'delevrence': 'Date de délivrance:',
            'email': 'Email:',
            'adresse': 'Adresse:',
            'adresse2': 'Adresse secondaire:',
            'pays': 'Pays:',
            'phone': 'Téléphone:',
            'image_user': 'Photo de profil:',
            
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['pays'].widget = CountrySelectWidget(attrs={'class': 'form-control'})
            self.fields['pays'].empty_label = '(choisissez un pays)'


class CommandeReservationFormclient(forms.ModelForm):
    class Meta:
        model = Commande_reservation
        fields = [ 'date_encharge', 'date_endepot','image_permit','matricule' ,'totalprix','available']
        
        widgets = {
            'date_encharge': forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'date_endepot': forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'matricule': forms.TextInput(attrs={'class':'form-control', 'readonly': 'readonly'}),
            'totalprix': forms.TextInput(attrs={'class':'form-control', 'readonly': 'readonly'}),
            'available': forms.CheckboxInput(),
        }
        labels={
            'date_encharge':' Date de depart:',
            'date_endepot': 'Date de retour:' ,
            'matricule': 'Immatriculation:',
            'totalprix':  'total du paye:',
            'available': 'Active:'
        }
    def clean(self):
        cleaned_data = super().clean()
        date_encharge = cleaned_data.get("date_encharge")
        date_endepot = cleaned_data.get("date_endepot")
        matricule = cleaned_data.get("matricule")
        totalprix = cleaned_data.get("totalprix")
        available = cleaned_data.get("available")

        if not date_encharge:
            self.add_error('date_encharge', "Ce champ est obligatoire.")
        if not date_endepot:
            self.add_error('date_endepot', "Ce champ est obligatoire.")
        if not matricule:
            self.add_error('matricule', "Ce champ est obligatoire.")
        if not totalprix:
            self.add_error('totalprix', "Ce champ est obligatoire.")
        if not available:
            self.add_error('available', "Vous devez sélectionner la case pour continuer.")
        
        return cleaned_data