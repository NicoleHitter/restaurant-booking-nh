from django.urls import path
from django.conf.urls.static import static
from . import views


app_name = 'restaurantbooking'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('reservations/', views.ReservationView.as_view(), name='reservations'),
    path('confirmation/', views.Confirmation.as_view(), name='confirmation'),    
    path('my_reservations/', views.ListReservationView.as_view(), name='my_reservations'),
    path('edit_reservations/<reservation_id>', views.edit_reservation_view, name='edit'),
    path('delete_reservation/<reservation_id>', views.delete_reservation, name='delete'),
]