from django.contrib import admin
from .models import Reservation, SignUp


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    model = Reservation
    list_display = ('name', 'email_address')

@admin.register(SignUp)
class SignUpAdmin(admin.ModelAdmin):
    
    model = SignUp
    list_display = ('first_name', 'last_name', 'email_address')