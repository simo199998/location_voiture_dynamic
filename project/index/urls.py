from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('home',views.home,name='home'),
    path('catalogue',views.catalogue,name='catalogue'),
    #path('select_car/<int:client_id>/',views.selecte_voiture,name='selecte'),
    path('maps',views.maps,name='maps'),
    
]