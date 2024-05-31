from django.core.management.base import BaseCommand
from index.models import Commande_reservation

class Command(BaseCommand):
    help = 'Handles overdue reservations'

    def handle(self, *args, **kwargs):
        Commande_reservation.handle_overdue_reservations()
        self.stdout.write(self.style.SUCCESS('Successfully handled overdue reservations'))
