from django import form
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User



GROUPSIZE_CHOICES = (
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    )

TIME_CHOICES = (
    ("12 PM", "12 PM"),
    ("12:30 PM", "12:30 PM"),
    ("1 PM", "1 PM"),
    ("1:30 PM", "1:30 PM"),
    ("2 PM", "2 PM"),
    ("2:30 PM", "2:30 PM"),
    ("3 PM", "3 PM"),
    ("3:30 PM", "3:30 PM"),
    ("4 PM", "4 PM"),
    ("4:30 PM", "4:30 PM"),
    ("5 PM", "5 PM"),
    ("5:30 PM", "5:30 PM"),
    ("6 PM", "6 PM"),
    ("6:30 PM", "6:30 PM"),
    ("7 PM", "7 PM"),
    ("7:30 PM", "7:30 PM"),
    ("8 PM", "8 PM"),
    ("8:30 PM", "8:30 PM"),
)


class Reservation(models.Model):
    """
    Model to be used in the forms.py and views.py for the booking form.
    It uses the User Foreign Key so that each book will be associated with a
    specific user.
    The rest of the information is saved for the booking
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=100, null=True, blank=True)
    groupsize = models.CharField(max_length=1, choices=GROUPSIZE_CHOICES, default="Group size", help_text='<br>Parties of'
                                        '<br>more than 10,'
                                        '<br>please call us on 021 4569 782')
    date = models.DateField(default=datetime.now)
    time = models.CharField(max_length=18, choices=TIME_CHOICES, default="12 PM")
    
    def __str__(self):
        return f"{self.user.name} | day: {self.day} | time: {self.time}"
