# reservations/forms.py
from django import forms
from .models import Commande_reservation
from administration.models import Voiture






'''class ClientForm(forms.Form):

    nom=forms.CharField(max_length=20)
    image=forms.ImageField()

    model = Client
        fields = [
            'nom', 'prenom', 'cin', 'naissance', 'permit', 'delevrence',
            'email', 'adresse', 'adresse2', 'pays', 'phone', 'image_permit'
        ]
    widgets = {
            'naissance': forms.DateInput(attrs={'type': 'date'}),
            'delevrence': forms.DateInput(attrs={'type': 'date'}),
        }

class UserForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Confirmez le mot de passe")

    class Meta:
        model = User
        fields = ['psw', 'email', 'nom']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Les mots de passe ne correspondent pas.")
        
        return cleaned_data'''

class CommandeReservationForm(forms.ModelForm):
    class Meta:
        model = Commande_reservation
        fields = [ 'date_encharge', 'date_endepot','image_permit','matricule' ,'totalprix']
        
        widgets = {
            'date_encharge': forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'date_endepot': forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'matricule': forms.TextInput(attrs={'class':'form-control'}),
            'totalprix': forms.TextInput(attrs={'class':'form-control'}),
        }
        labels={
            'date_encharge':' Date de depart:',
            'date_endepot': 'Date de retour:' ,
            'matricule': 'Immatriculation:',
            'totalprix':  'total du paye:',
        }