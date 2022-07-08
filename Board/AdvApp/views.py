from django.shortcuts import render

from django.views.generic import ListView
from .models import *

class AdvertList(ListView):
    model = Advert
    template_name = 'adverts.html'
    context_object_name = 'advertList'
    queryset = Advert.objects.order_by('-id_category')

