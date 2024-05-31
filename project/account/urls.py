from django.urls import path
from . import views


urlpatterns = [
       path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/<int:client_id>/', views.profile, name='profile'),
   path('update_profile/', views.update_profile, name='update_profile'),
   path('selecte_voiture/<int:client_id>/',views.selecte_voiture,name='selecte_voiture'),
   path('logout/', views.user_logout, name='logout'),
    path('delete_reservation/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    
]