# your_app/management/commands/check_dates_and_notify.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from administration.models import Assurance, VisiteTechnique, Vignette, User, Notification

class Command(BaseCommand):
    help = 'Check dates and send notifications if needed'

    def handle(self, *args, **kwargs):
        now = timezone.now().date()
        notify_date = now + timedelta(days=5)

        assurances = Assurance.objects.filter(date_fin=notify_date)
        visites_techniques = VisiteTechnique.objects.filter(date_fin=notify_date)
        vignettes = Vignette.objects.filter(date_fin=notify_date)

        for assurance in assurances:
            for user in User.objects.all():
                Notification.objects.create(user=user, message=f"L'assurance pour la voiture {assurance.voiture.marque} expire bientôt.")

        for visite in visites_techniques:
            for user in User.objects.all():
                Notification.objects.create(user=user, message=f"La visite technique pour la voiture {visite.voiture.marque} expire bientôt.")

        for vignette in vignettes:
            for user in User.objects.all():
                Notification.objects.create(user=user, message=f"La vignette pour la voiture {vignette.voiture.marque} expire bientôt.")

        self.stdout.write(self.style.SUCCESS('Successfully sent notifications'))
