# project/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Réglages par défaut de Django pour Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

# Utiliser une chaîne ici signifie que le worker n'a pas besoin
# de sérialiser l'objet de configuration au format JSON.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Charger les tâches des applications enregistrées
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
