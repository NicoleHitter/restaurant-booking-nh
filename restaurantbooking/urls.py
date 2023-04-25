from django.urls import path
from . import views


app_name = 'restaurantbooking'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('reservations/', views.ReservationView.as_view(), name='reservations'),
    path('confirmation/', views.Confirmation.as_view(), name='confirmation'),    
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
]