# project/__init__.py

from __future__ import absolute_import, unicode_literals

# Assurez-vous que l'application Celery est chargée
from .celery import app as celery_app

__all__ = ('celery_app',)
