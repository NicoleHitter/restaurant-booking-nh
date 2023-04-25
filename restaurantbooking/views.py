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

class ListReservationView(generic.DetailView):
    """
    This is the view that will bring up the
    list of bookings for a particular users
    so that they can be edited or deleted
    """

    template_name = 'my_reservations.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            reservations = Reservation.objects.filter(user=request.user)

            return render(request, 'my_reservations.html', {
                'reservations': reservations
            }
            )
        else:
            return redirect('account_login')


@login_required
def edit_reservation_view(request, reservation_id):
    """
    When a user is on the My Bookings page
    which can only be accessed if you are
    logged in, they can click on the edit button.
    This will bring them to a new page, where the booking
    they wish to edit, located using the booking id,
    appears, prepopulated with the current information.
    Once the user clicks on the submit changes button
    they will be redirected to the home page and a
    confimation message will appear.
    """

    if request.user.is_authenticated:
        reservation = get_object_or_404(Reservation, id=reservation_id)
        if reservation.user == request.user:
            if request.method == 'POST':
                form = OnlineForm(data=request.POST, instance=reservation)
                if form.is_valid():
                    form.save()
                    # Pops up a message to the user when a booking is edited
                    messages.success(request, 'Your reservation has been updated')
                    return redirect('/')
        else:
            messages.error(request, 'You do not have the authority to access this page!')
            return redirect('/')

    form = OnlineForm(instance=reservation)

    return render(request, 'edit_reservations.html', {
        'form': form
        })


@login_required
def delete_reservation(request, reservation_id):
    """
    When a user is on the My Bookings page
    which can only be accessed if you are
    logged in, they can click on the cancel booking
    button. This will cancel the booking using its
    booking id, redirect the user back to the home page and
    pop up a confimation message will appear.
    """
    if request.user.is_authenticated:
        reservation = get_object_or_404(Reservation, id=reservation_id)
        if reservation.user == request.user:
            reservation.delete()
            # Pops up a message to the user when a bookings is cancelled
            messages.success(request, 'Your reservation has been cancelled')
            return redirect('/')
        else:
            messages.error(request, 'You do not have the authority to access this page!')
            return redirect('/')

class SignUpView(FormView):
    """
    Renders the Sign up form page in the browser
    Using the SignUpForm created in the forms.py file
    When the Sign up form is completed and submitted
    the user will receive a message to say it was
    successful.
    """
    template_name = 'sign_up.html'
    form_class = SignUpForm

    def sign_up_view(self, request):
        return render(request, 'sign_up.html')

    def post(self, request):
        """
        Uses the SignUpForm from forms.py
        Checks if all the infromation in valid
        and then saves it to the database.
        Once the information is saved the site
        visitor will receive a pop up message
        """
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
        # Pops up a message to the site visitor when their information
        # has been saved
        messages.success(request, 'Thank you for signing up to our newsletter')
        return redirect('/')
