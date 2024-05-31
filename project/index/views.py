from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from administration.models import Voiture
from .models import Commande_reservation
import datetime
from datetime import *
from .forms import CommandeReservationForm
from account.models import Client



# Create your views here.
def home(request):
        voiture=Voiture.objects.all()
        
        return render(request,'index/home.html',{'voiture':voiture})
def catalogue(request):
            cata_data=[]
            lenght=Voiture.objects.count()
            voitures=Voiture.objects.all()
            for voiture in voitures:
                        marque=voiture.marque
                        type_voiture=voiture.type
                        carburant=voiture.type_carburant
                        boite=voiture.boite_vitesse
                        model=voiture.model
                        prix=voiture.prix
                        disponibilite=voiture.disponibilite
                        matricule=voiture.matricule
                        image=voiture.image.url
                        cata_data.append({'marque':marque,'type':type_voiture,'image':image,'carburant':carburant,'boite':boite,'model':model,'prix':prix,'matricule':matricule,'disponibilite':disponibilite})
            
            return render(request,'index/catalogue.html',{'cata_data':cata_data,'lenght':lenght})

def maps(request):
        return render(request,'index/maps.html')





