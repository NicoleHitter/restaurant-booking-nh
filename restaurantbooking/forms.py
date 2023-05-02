from django.forms import ModelForm
from django.core import validators
from django import forms
from .models import Reservation


class DateInput(forms.DateInput):
    """
    This class provides a widget for use in the
    booking form. It provides a calendar for users
    to pick the booking date from
    """
    input_type = 'date'


class OnlineForm(ModelForm):
    """
    This form is connected with the view
    in order to provide users with the neccessary
    fields for making a reservation
    It also provides the labels and placeholder
    text for each field, as wells as the widgets
    and handles validation where required.
    """
    name = forms.CharField(
        label='Reservation Name',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Reservation Name'}),
    )

    email_address = forms.EmailField(
        label='Email Address',
        required=True,
        validators=[validators.EmailValidator(
            message="Invalid Email Address")],
        widget=forms.TextInput(attrs={'placeholder': 'Email Address'}),
    )

    class Meta:
        """Defines which model to pull the
        fields from"""
        model = Reservation
        # Tell the form to use all the fields provided
        fields = '__all__'
        # Except for the user field
        exclude = ('user', )
        widgets = {
            'date': DateInput()
        }
