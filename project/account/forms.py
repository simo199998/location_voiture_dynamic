from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Client
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhonePrefixSelect
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='Mot de passe :',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirmer le mot de passe :',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Entrez le même mot de passe que précédemment, pour vérification."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password1') != cd.get('password2'):
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cd.get('password2')

'''class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),label='Mot de passe :')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirmer le mot de passe')


    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError("Passwords don't match.")
        return cd.get('password2')
    
'''
'''class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'cin', 'naissance', 'permit', 'delevrence', 'email', 'adresse', 'adresse2', 'pays', 'phone', 'image_user']
'''





class ClientForm(forms.ModelForm):
    nom = forms.CharField(
        label='Nom',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        
    )
    prenom = forms.CharField(
        label='Prénom',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        
    )
    cin = forms.CharField(
        label='CIN',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        
    )
    naissance = forms.DateField(
        label='Date de naissance',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        
    )
    permit = forms.CharField(
        label='Numéro de permis',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        
    )
    delevrence = forms.DateField(
        label='Date de délivrance',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        
    )
    adresse = forms.CharField(
        label='Adresse',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        
    )
    adresse2 = forms.CharField(
        label='Complément d\'adresse',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Entrez un complément d'adresse si nécessaire.",
        required=False
    )
    pays = CountryField(blank_label='(choisissez un pays)').formfield(
        widget=CountrySelectWidget(attrs={'class': 'form-control'})
    )

    phone = PhoneNumberField(
        label='Numéro de téléphone',
        widget=PhoneNumberPrefixWidget(initial='MA', attrs={'class': 'form-control d-inline-block w-auto'}),
        
    )
    image_user = forms.ImageField(
        label='Photo de profil',
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        help_text="Téléchargez une photo de profil.",
        required=False
    )

    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'cin', 'naissance', 'permit', 'delevrence', 'email', 'adresse', 'adresse2', 'pays', 'phone', 'image_user']



class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Nom d’utilisateur', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={'class': 'form-control'}))



class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'cin', 'naissance', 'permit', 'delevrence', 'email', 'adresse', 'adresse2', 'pays', 'phone', 'image_user']