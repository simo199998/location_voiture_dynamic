from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, ClientForm, UserLoginForm,ClientUpdateForm
from index.forms import CommandeReservationForm
from index.models import Commande_reservation,Notification
from .models import Client
from administration.models import Voiture
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        client_form = ClientForm(request.POST, request.FILES)
        if user_form.is_valid() and client_form.is_valid():
            
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            client = client_form.save(commit=False)
            client.user = user
            client.save()
            Commande_reservation.objects.create( client=client)
            login(request, user)
            return redirect('login')
    else:
        user_form = UserRegisterForm()
        client_form = ClientForm()
    return render(request, 'account/register.html', {'user_form': user_form, 'client_form': client_form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile', client_id=request.user.client_profile.id)
    else:
        form = UserLoginForm()
    return render(request, 'account/login.html', {'form': form})

def profile(request, client_id):
    client = get_object_or_404(Client, id=client_id, user=request.user)
    voiture_reservation = None

    try:
        voiture_reservation = Commande_reservation.objects.get(client=client)
    except Commande_reservation.DoesNotExist:
        pass
    return render(request, 'account/profile.html', {'client':client,'voiture': voiture_reservation})



def update_profile(request):
    client_profile = request.user.client_profile
    if request.method == 'POST':
        form = ClientUpdateForm(request.POST, request.FILES, instance=client_profile)
        if form.is_valid():
            form.save()
            return redirect('profile', client_id=request.user.client_profile.id)
    else:
        form = ClientUpdateForm(instance=client_profile)
    return render(request, 'account/update_profile.html', {'form': form})

def selecte_voiture(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        reservation_form = CommandeReservationForm(request.POST, request.FILES)
        
        if reservation_form.is_valid():
            matricule_voiture = reservation_form.cleaned_data['matricule']
            voiture = Voiture.objects.get(matricule=matricule_voiture)
            
            
            voiture.disponibilite='NON'
            voiture.save()
            
            reservation = reservation_form.save(commit=False)
            reservation.client = client  # Associer le client à la réservation
            reservation.voiture = voiture
            reservation.save()
            for user in User.objects.all():
                Notification.objects.create(user=user, message=f"client  {client} demande le reservation la voiture {voiture.marque} {voiture.type}.")
            return redirect('profile', client_id=client.id)  
    else:
        reservation_form = CommandeReservationForm()
    
    return render(request, 'account/selecte_voiture.html', {'reservation_form': reservation_form, 'client': client})


def user_logout(request):
    logout(request)
    return redirect('login')


def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Commande_reservation, id=reservation_id)
    client_id = reservation.client.id
    voiture = reservation.voiture
    if voiture:
        voiture.disponibilite = 'OUI'
        voiture.save()
    reservation.delete()
    for user in User.objects.all():
                Notification.objects.create(user=user, message=f"client  {client_id} annule le reservation la voiture {voiture.marque} {voiture.type}.")
    return redirect('profile', client_id=client_id)

