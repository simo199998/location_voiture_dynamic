# administration/context_processors.py

from index.models import Commande_reservation,Voiture
from .forms import UpdateDateForm

def global_count(request):
    commande = Commande_reservation.objects.all()
    commande_count = commande.count()
    voiture_dispo = Voiture.objects.all()
    available_count = sum(1 for voiture in voiture_dispo if voiture.disponibilite.lower() == 'oui')
    forms = {res.pk: UpdateDateForm(instance=res) for res in commande}
    return {
        'commande_count': commande_count,
        
        'available_count': available_count
    }
