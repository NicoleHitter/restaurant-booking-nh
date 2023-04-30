from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField



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
   
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email_address = models.EmailField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    group_size = models.CharField(max_length=1, choices=GROUPSIZE_CHOICES, 
                                 default="Group size", 
                                 help_text='<br>Parties of'
                                 '<br>more than 10,'
                                 '<br>please call us on 021 4569 782')
    date = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="12 PM")
    comment = models.CharField(max_length=100, 
                               help_text='Please let us know if you have any special requirements', 
                               default="Please add your comment here")


    class Meta:
        constraints = [
                models.UniqueConstraint(fields=['user', 'date', 'time'], name='reservation_user_uniq')
        ]
    
    def __str__(self):
        return self.name

