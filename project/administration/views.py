from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .forms import VoitureForm, AssuranceForm, VisiteTechniqueForm, VignetteForm,CommandeReservationFormclient,UpdateDateForm,AdminLoginForm,ClientProfileForm,CommandeReservationForm
from index.models import Commande_reservation,ArchiveReservation
from django.contrib.auth import authenticate, login, logout
from . models import Voiture,VisiteTechnique,Vignette,Assurance
from datetime import*
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import base64
from django.contrib.auth.models import User
from .models import Notification
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('reservation_statistiques')
            else:
                form.add_error(None, "Invalid credentials or not an admin.")
    else:
        form = AdminLoginForm()
    return render(request, 'administration/admin_login.html', {'form': form})

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

# Create your views here.
@login_required
def home(request):
            if not request.user.is_staff:
                return redirect('admin_login')
            commande=Commande_reservation.objects.all()
            date_now = datetime.now() 
            current_time = datetime.now().time()
            target_time = datetime.strptime("08:35:00", "%H:%M:%S").time()
            
            for i in commande:
                date_fin=datetime.strptime(str(i.date_endepot), '%Y-%m-%d')
                if date_now >= date_fin and current_time >= target_time  and i.available:
                    i.delete()
                    dispo=Voiture.objects.get(matricule=str(i.matricule) )
                    print(dispo)
                    dispo.disponibilite='oui'
                    dispo.save()
                    for user in User.objects.all():
                        Notification.objects.create(user=user, message=f"commande {i.voiture.marque} a été expires.")
                    return redirect('index')
                
            commande_count=Commande_reservation.objects.count()
            voiture_dispo=Voiture.objects.all()
            available_count = sum(1 for voiture in voiture_dispo if voiture.disponibilite.lower() == 'oui')
            forms = {res.pk: UpdateDateForm(instance=res) for res in commande}
            
            return render(request,'administration/index.html',{'forms': forms,'commande':commande,'voiture_dispo':voiture_dispo,'commande_count':commande_count,'available_count':available_count})
@login_required
def ajoute_voiture(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    if request.method == 'POST':
        voiture_form = VoitureForm(request.POST, request.FILES)
        assurance_form = AssuranceForm(request.POST)
        visite_technique_form = VisiteTechniqueForm(request.POST)
        vignette_form = VignetteForm(request.POST)
        
        if voiture_form.is_valid() and assurance_form.is_valid() and visite_technique_form.is_valid() and vignette_form.is_valid():
            voiture = voiture_form.save()
            
            assurance = assurance_form.save(commit=False)
            assurance.voiture = voiture
            assurance.save()

            visite_technique = visite_technique_form.save(commit=False)
            visite_technique.voiture = voiture
            visite_technique.save()

            vignette = vignette_form.save(commit=False)
            vignette.voiture = voiture
            vignette.save()
            for user in User.objects.all():
                Notification.objects.create(user=user, message=f"Une nouvelle voiture {voiture.marque} a été ajoutée.")
            return redirect('index')
    else:
        voiture_form = VoitureForm()
        assurance_form = AssuranceForm()
        visite_technique_form = VisiteTechniqueForm()
        vignette_form = VignetteForm()

    context = {
        'voiture_form': voiture_form,
        'assurance_form': assurance_form,
        'visite_technique_form': visite_technique_form,
        'vignette_form': vignette_form,
    }
    
    return render(request, 'administration/ajoute_voiture.html', context)
@login_required
def voitures(request):
      if not request.user.is_staff:
        return redirect('admin_login')
      voitures=Voiture.objects.all()
      number_voiture=Voiture.objects.count()
      return render(request,'administration/voitures.html',{'voitures':voitures,'number_voiture':number_voiture})
@login_required
def fiche_voiture(request,pk):
      if not request.user.is_staff:
        return redirect('admin_login')
      voiture = get_object_or_404(Voiture, pk=pk)
      visite=get_object_or_404(VisiteTechnique, pk=pk)
      assurance=get_object_or_404(Assurance, pk=pk)
      vignette=get_object_or_404(Vignette, pk=pk)
      return render(request,'administration/fiche_voiture.html',{'voiture': voiture,'visite':visite,'assurance':assurance,'vignette':vignette})
@login_required
def update_voiture(request,pk):
    if not request.user.is_staff:
        return redirect('admin_login')
    voiture = get_object_or_404(Voiture, pk=pk)
    if request.method == "POST":
        form = VoitureForm(request.POST, instance=voiture)
        #form_visite = VisiteTechniqueForm(request.POST, instance=voiture)
        #form_assurance = VisiteTechniqueForm(request.POST, instance=voiture)
        #form_vignette = VignetteForm(request.POST, instance=voiture)  
        if form.is_valid() :
            form.save() 
            #form_visite.save()
            #form_assurance.save()
            #form_vignette.save()
            for user in User.objects.all():
                Notification.objects.create(user=user, message=f"Voiture {voiture.marque} a été mise à jour.")
            return redirect('fiche_voiture', pk=voiture.pk)  
    else:
        form = VoitureForm(instance=voiture)
        #form_visite=VisiteTechniqueForm(instance=voiture)
        #form_assurance=AssuranceForm(instance=voiture)
        #form_vignette=VignetteForm(instance=voiture)
    
    return render(request,'administration/update_voiture.html',{'form':form})

def delete_voiture(request, pk):
    voiture = get_object_or_404(Voiture, pk=pk)
    if request.method == "POST":
        voiture.delete()
        for user in User.objects.all():
            Notification.objects.create(user=user, message=f"Voiture {voiture.marque} a été supprimée.")
            
        return redirect('voitures')  # Redirigez vers la liste des voitures après suppression
    return render(request, 'administration/voitures.html', {'voiture': voiture})
def demmande_enligne(request):
     if not request.user.is_staff:
        return redirect('admin_login')
     commande=Commande_reservation.objects.all()
    
     return render(request,'administration/demmande_enligne.html',{'commande':commande})

@login_required
def approve_reservation(request, pk):
    if not request.user.is_staff:
        return redirect('admin_login')
    reservation = get_object_or_404(Commande_reservation, pk=pk)
    if request.method == 'POST':
        if 'approve' in request.POST:
            reservation.available = True
            reservation.save()
            for user in User.objects.all():
                Notification.objects.create(user=user, message=f"La réservation de {reservation.client.nom} {reservation.client.prenom} a été approuvée.")
            return redirect('index')  # Adjust this to your list view
        elif 'disapprove' in request.POST:
            reservation.delete()
            return redirect('demmande')
    else:
        form = CommandeReservationForm(instance=reservation)
    return render(request, 'administration/approve_reservation.html', {'form': form, 'reservation': reservation})




def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    result = pisa.CreatePDF(html, dest=response)
    if result.err:
        return HttpResponse('Error generating PDF', status=400)
    return response

def download_contract(request, pk):
    reservation = get_object_or_404(Commande_reservation, pk=pk)
    base64_image = None
    if reservation.image_permit:
        with open(reservation.image_permit.path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    context = {
        'reservation': reservation,
        'client': reservation.client,
        'voiture': reservation.voiture,
        'base64_image': base64_image,
    }
    return render_to_pdf('administration/contrat.html', context)
    '''reservation = get_object_or_404(Commande_reservation, pk=pk)
    context = {
        'reservation': reservation,
        'client': reservation.client,
        'voiture': reservation.voiture,
        'image':reservation.image_permit.url
        # Add more context if needed
    }'''
    

def update_dates(request, pk):
    reservation = get_object_or_404(Commande_reservation, pk=pk)
    if request.method == 'POST':
        form = UpdateDateForm(request.POST, instance=reservation)
        if form.is_valid():
            reservation = form.save(commit=False)
            # Recalcule du prix total
            nombre_de_jours = (reservation.date_endepot - reservation.date_encharge).days
            voiture_prix = reservation.voiture.prix
            reservation.totalprix = str(int(reservation.totalprix) + nombre_de_jours * int(voiture_prix))
            reservation.save()
            return redirect('index')  # Assurez-vous que le nom de votre URL principale est 'index'
    return redirect('index')  # Redirige même en cas d'échec pour simplifier




from account.models import Client
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth
from django.db.models import Sum,FloatField
import json
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from django.db.models.functions import TruncDay,Cast
from django.utils.timezone import make_aware
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth
from collections import defaultdict
@login_required
def reservation_statistiques_view(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    notifications = Notification.objects.filter(user=request.user, read=False).order_by('-created_at')
    total_voitures = Voiture.objects.count()
    voitures_reservees = Commande_reservation.objects.filter(voiture__isnull=False, available=True).count()
    voitures_non_reservees = total_voitures - voitures_reservees
    #charts
    reservations_per_month = (
        ArchiveReservation.objects
        .annotate(month=TruncMonth('date_reservation'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # Prepare data for the monthly bar chart
    monthly_labels = []
    monthly_data = []

    # Use a dictionary to store the counts
    monthly_data_dict = defaultdict(int)

    for entry in reservations_per_month:
        month_str = entry['month'].strftime('%B %Y')
        monthly_data_dict[month_str] = entry['count']

    sorted_monthly_data = dict(sorted(monthly_data_dict.items(), key=lambda x: datetime.strptime(x[0], '%B %Y')))

    for month, count in sorted_monthly_data.items():
        monthly_labels.append(month)
        monthly_data.append(count)

    monthly_labels_json = json.dumps(monthly_labels)
    monthly_data_json = json.dumps(monthly_data)

    # Query the database for daily reservations
    reservations_per_day = (
        ArchiveReservation.objects
        .annotate(day=TruncDay('date_reservation'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    # Prepare data for the daily bar chart
    daily_labels = []
    daily_data = []

    # Use a dictionary to store the counts
    daily_data_dict = defaultdict(int)

    for entry in reservations_per_day:
        day_str = entry['day'].strftime('%Y-%m-%d')
        daily_data_dict[day_str] = entry['count']

    sorted_daily_data = dict(sorted(daily_data_dict.items(), key=lambda x: datetime.strptime(x[0], '%Y-%m-%d')))

    for day, count in sorted_daily_data.items():
        daily_labels.append(day)
        daily_data.append(count)

    daily_labels_json = json.dumps(daily_labels)
    daily_data_json = json.dumps(daily_data)
    #fin
    #price
    daily_datas = (ArchiveReservation.objects
                  .annotate(day=TruncDay('date_reservation'))
                  .values('day')
                  .annotate(total_prix=Sum('totalprix'))
                  .order_by('day'))

    daily_dates = [item['day'].strftime("%Y-%m-%d") for item in daily_datas]
    daily_totals = [item['total_prix'] for item in daily_datas]

    # Agréger les données par mois
    mois_data = (ArchiveReservation.objects
                 .annotate(month=TruncMonth('date_reservation'))
                 .values('month')
                 .annotate(total_prix=Sum('totalprix'))
                 .order_by('month'))

    mois_dates = [item['month'].strftime("%Y-%m") for item in mois_data]
    mois_totals = [item['total_prix'] for item in mois_data]

    
    #finprice
    assurance=Assurance.objects.all()
    messages = []
    date_now = datetime.now()
    date_24h = date_now + timedelta(days=2)
    date_24h_str = date_24h.strftime('%Y-%m-%d')
    for i in assurance:
        date_fin=datetime.strptime(str(i.date_fin), '%Y-%m-%d')
        date_fin_str=date_fin.strftime('%Y-%m-%d')
        
        if date_fin_str==date_24h_str:
            messages.append(f"l'assurance du {i.voiture.marque} {i.voiture.type} matricule{i.voiture.matricule} experie le {i.date_fin}")
    visite=VisiteTechnique.objects.all()
    for i in visite:
        date_fin=datetime.strptime(str(i.date_fin), '%Y-%m-%d')
        date_fin_str=date_fin.strftime('%Y-%m-%d')
        
        if date_fin_str==date_24h_str:
            messages.append(f"la visite technique du {i.voiture.marque} {i.voiture.type} matricule{i.voiture.matricule} experie le {i.date_fin}")
    visite=Vignette.objects.all()
    for i in visite:
        date_fin=datetime.strptime(str(i.date_fin), '%Y-%m-%d')
        date_fin_str=date_fin.strftime('%Y-%m-%d')
        
        if date_fin_str==date_24h_str:
            messages.append(f"la vignette du {i.voiture.marque} {i.voiture.type} matricule{i.voiture.matricule} experie le {i.date_fin}")
    context = {
        'notifications': notifications,
        'voitures_reservees': voitures_reservees,
        'voitures_non_reservees': voitures_non_reservees,
        'monthly_labels_json': json.dumps(monthly_labels),
        'monthly_data_json': json.dumps(monthly_data),
        'daily_labels_json': json.dumps(daily_labels),
        'daily_data_json': json.dumps(daily_data),
        'messages':messages,
        'daily_dates_json': json.dumps(daily_dates),
        'daily_totals_json': json.dumps(daily_totals),
        'mois_dates_json': json.dumps(mois_dates),
        'mois_totals_json': json.dumps(mois_totals)
        
        
    }
    return render(request, 'administration/table_borde.html', context)

@login_required
def document_vehicule_view(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    today = datetime.now().date()
    target_date = today + timedelta(days=5)

    voitures_expirations = []

    assurances = Assurance.objects.filter(date_fin__lte=target_date, date_fin__gte=today - timedelta(days=1))
    visites_techniques = VisiteTechnique.objects.filter(date_fin__lte=target_date, date_fin__gte=today - timedelta(days=1))
    vignettes = Vignette.objects.filter(date_fin__lte=target_date, date_fin__gte=today - timedelta(days=1))

    for assurance in assurances:
        voitures_expirations.append(assurance.voiture)

    for visite in visites_techniques:
        voitures_expirations.append(visite.voiture)

    for vignette in vignettes:
        voitures_expirations.append(vignette.voiture)

    # Éliminer les doublons
    voitures_expirations = list(set(voitures_expirations))

    context = {
        'voitures_expirations': voitures_expirations,
    }

    return render(request, 'administration/documents_vihecule.html', context)
@login_required
def update_documents_view(request, voiture_id):
    if not request.user.is_staff:
        return redirect('admin_login')
    voiture = get_object_or_404(Voiture, id=voiture_id)
    
    today = datetime.now().date()
    target_date = today + timedelta(days=5)

    try:
        assurance = Assurance.objects.get(voiture=voiture, date_fin__lte=target_date, date_fin__gte=today - timedelta(days=1))
    except Assurance.DoesNotExist:
        assurance = None
    
    try:
        visite_technique = VisiteTechnique.objects.get(voiture=voiture, date_fin__lte=target_date, date_fin__gte=today - timedelta(days=1))
    except VisiteTechnique.DoesNotExist:
        visite_technique = None
    
    try:
        vignette = Vignette.objects.get(voiture=voiture, date_fin__lte=target_date, date_fin__gte=today - timedelta(days=1))
    except Vignette.DoesNotExist:
        vignette = None
    
    if request.method == 'POST':
        assurance_form = AssuranceForm(request.POST, instance=assurance)
        visite_technique_form = VisiteTechniqueForm(request.POST, instance=visite_technique)
        vignette_form = VignetteForm(request.POST, instance=vignette)
        
        if all([form.is_valid() for form in [assurance_form, visite_technique_form, vignette_form] if form is not None]):
            if assurance_form.is_valid():
                assurance = assurance_form.save(commit=False)
                assurance.voiture = voiture
                assurance.save()

            if visite_technique_form.is_valid():
                visite_technique = visite_technique_form.save(commit=False)
                visite_technique.voiture = voiture
                visite_technique.save()

            if vignette_form.is_valid():
                vignette = vignette_form.save(commit=False)
                vignette.voiture = voiture
                vignette.save()

            return redirect('document_vehicule_view')
    else:
        assurance_form = AssuranceForm(instance=assurance) if assurance else None
        visite_technique_form = VisiteTechniqueForm(instance=visite_technique) if visite_technique else None
        vignette_form = VignetteForm(instance=vignette) if vignette else None
    
    context = {
        'voiture': voiture,
        'assurance_form': assurance_form,
        'visite_technique_form': visite_technique_form,
        'vignette_form': vignette_form,
    }
    
    return render(request, 'administration/update_documents.html', context)

@login_required
def client(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    client=Client.objects.all()
    return render(request,'administration/clients.html',{'client':client})
@login_required
def client_profile(request, id):
    if not request.user.is_staff:
        return redirect('admin_login')
    client = get_object_or_404(Client, id=id)
    reservations = ArchiveReservation.objects.filter(client=client)
    reservation_details = []

    for reservation in reservations:
        has_passed = reservation.date_endepot > date.today() if reservation.date_endepot else False
        
        if reservation.date_endepot< date.today():
            reservation.available=False
            reservation.disponibilite=='oui'
            reservation.save()
        reservation_details.append({
            'reservation': reservation,
            'has_passed': has_passed
        })
    reservation_details.sort(key=lambda x: not x['has_passed'])  # Show passed reservations at the bottom
    return render(request, 'administration/client_profile.html', {'client': client, 'reservation_details': reservation_details,'has_passed': has_passed})
@login_required
def update_client_profile(request, id):
    if not request.user.is_staff:
        return redirect('admin_login')
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        form = ClientProfileForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_profile', id=client.id)  # Redirect to the client profile page after saving
    else:
        form = ClientProfileForm(instance=client)
    return render(request, 'administration/update_client_profile.html', {'form': form, 'client': client})
@login_required
def selecte_voiture_admin(request, id):
    if not request.user.is_staff:
        return redirect('admin_login')
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        reservation_form = CommandeReservationFormclient(request.POST, request.FILES)
        if reservation_form.is_valid():
            matricule_voiture = reservation_form.cleaned_data['matricule']
            voiture = Voiture.objects.get(matricule=matricule_voiture)
            voiture.disponibilite = 'NON'
            voiture.save()
            reservation = reservation_form.save(commit=False)
            reservation.client = client  # Associate the client with the reservation
            reservation.voiture = voiture
            reservation.save()
            for user in User.objects.all():
                Notification.objects.create(user=user, message=f"Client {client.nom} {client.prenom} demande la réservation de la voiture {voiture.marque} {voiture.type}.")
            return redirect('index')
    else:
        reservation_form = CommandeReservationFormclient()
    return render(request, 'administration/selecte_voiture_admin.html', {'reservation_form': reservation_form, 'client': client})


