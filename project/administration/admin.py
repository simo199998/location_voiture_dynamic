from django.contrib import admin
from . models import Vignette,VisiteTechnique,Voiture,Assurance
# Register your models here.
admin.site.register(VisiteTechnique)
admin.site.register(Vignette)
admin.site.register(Voiture)
admin.site.register(Assurance)