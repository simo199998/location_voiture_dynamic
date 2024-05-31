# management/commands/delete_expired_notifications.py
import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from administration.models import Notification

class Command(BaseCommand):
    help = 'Delete notifications older than 48 hours'

    def handle(self, *args, **kwargs):
        expiration_time = timezone.now() - datetime.timedelta(hours=48)
        expired_notifications = Notification.objects.filter(created_at__lt=expiration_time)
        count = expired_notifications.count()
        expired_notifications.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} expired notifications'))
