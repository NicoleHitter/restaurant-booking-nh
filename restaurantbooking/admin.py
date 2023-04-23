from django.contrib import admin
from .models import Reservation
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Reservation)
class ReservationAdmin(SummernoteModelAdmin):

    summernote_fields = ('content',)

