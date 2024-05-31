from django.urls import path,re_path
from . import views
 
urlpatterns = [
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('index',views.home,name='index'),
    path('ajoute_voiture',views.ajoute_voiture,name='ajoute_voiture'),
    path('voitures',views.voitures,name='voitures'),
    path('fiche_voiture/<int:pk>/', views.fiche_voiture, name='fiche_voiture'),
    path('voiture/<int:pk>/update/',views.update_voiture, name='update_voiture'),
    path('voiture/<int:pk>/delete/', views.delete_voiture, name='delete_voiture'),
    path('demmande',views.demmande_enligne,name='demmande'),
     path('approve_reservation/<int:pk>/', views.approve_reservation, name='approve_reservation'),
     path('download_contract/<int:pk>/', views.download_contract, name='download_contract'),
     path('reservation-statistiques/', views.reservation_statistiques_view, name='reservation_statistiques'),
     path('update_dates/<int:pk>/', views.update_dates, name='update_dates'),
    path('documents-vehicule/', views.document_vehicule_view, name='document_vehicule_view'),
    path('update-documents/<int:voiture_id>/', views.update_documents_view, name='update_documents_view'),
    path('client', views.client, name='client'),
    path('clients/<int:id>/', views.client_profile, name='client_profile'),
    path('clients/<int:id>/edit/', views.update_client_profile, name='update_client_profile'),
    path('clients/<int:id>/selecte_voiture/', views.selecte_voiture_admin, name='selecte_voiture_admin'),
]
