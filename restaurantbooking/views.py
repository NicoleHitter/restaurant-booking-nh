from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from .forms import OnlineForm, SignUpForm
from .models import Reservation


class Home(generic.DetailView):
    """
    Renders the Index page in the browser
    """
    template_name = 'index.html'

# The get request returns the template set out above
# In this case it was the index.html template
    def get(self, request):
        return render(request, 'index.html')


class ReservationView(FormView):
    """
    Renders the ReservationForm page in the browser
    Using the OnlineForm created in the forms.py file
    When the booking form is completed and submitted
    the user is redirected to a confirmation page.
    """
    template_name = 'reservations.html'
    form_class = OnlineForm
    success_url = '/confirmation/'

    def reservation_view(self, request):
        return render(request, 'reservations.html')

    def post(self, request):
       
        form = OnlineForm(data=request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return render(request, 'confirmation.html')
        else:
            messages.error(request, 'Reservation not completed, please check your information')

        return render(request, 'reservations.html', {
                'form': form
                }
                )    


class Confirmation(generic.DetailView):
    """
    Renders the Confirmation page in the browser
    """
    template_name = 'confirmation.html'

    def get(self, request):
        return render(request, 'confirmation.html')

class SignIn(generic.DetailView):
    """
    Renders the Login page in the browser
    """

    def login_view(self, request):
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            return render(request, 'login.html')
