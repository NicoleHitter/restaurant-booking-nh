from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
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

