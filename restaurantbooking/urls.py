from django.urls import path
from . import views


app_name = 'restaurantbooking'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('reservations/', views.ReservationView.as_view(), name='reservations'),
    path('confirmation/', views.Confirmation.as_view(), name='confirmation'),    
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('my_reservations/', views.ListReservationView.as_view(), name='my_reservations'),
    path('edit_reservations/<reservation_id>', views.edit_reservation_view, name='edit'),
    path('delete_reservation/<reservation_id>', views.delete_reservation, name='delete'),
]