from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import CreateAdvertForm, CreateResponseForm
from .filters import ResponseFilter
from django.shortcuts import redirect
from datetime import datetime


class AdvertList(ListView):
    model = Advert
    template_name = 'adverts.html'
    context_object_name = 'advertList'
    queryset = Advert.objects.order_by('-dateCreation')


class AdvertView(DetailView):
    model = Advert
    template_name = 'advert.html'
    form_class = CreateResponseForm
    context_object_name = 'advertView'
    queryset = Advert.objects.all()

    def post(self, request, *args, **kwargs):
        response = Response(
            id_user=request.user,
            id_advert=Advert.objects.get(pk=request.POST['id_advert']),
            text=request.POST['text'],
        )
        response.save()

        return redirect('/advert/' + str(response.id_advert.pk))

class AdvertCreate(CreateView):
    template_name = 'add.html'
    form_class = CreateAdvertForm

    def post(self, request, *args, **kwargs):
        advert = Advert(
            id_user=request.user,
            id_category=request.POST['category'],
            title = request.POST['title'],
            text=request.POST['text'],
            image = request.POST['image'],
            file=request.POST['file']
        )
        advert.save()

        return redirect('/adverts/')



class AdvertUpdate(UpdateView):
    template_name = 'edit.html'
    form_class = CreateAdvertForm
 
    
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Advert.objects.get(pk=id)


class ResponseList(ListView):
    model = Response
    template_name = 'response.html'
    context_object_name = 'responseList'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_adverts = Advert.objects.filter(id_user=self.request.user)
        query = Response.objects.filter(id_advert__in=user_adverts).order_by('-id_user')
        context['filter'] = ResponseFilter(self.request.GET, queryset=query)
        return context


class ResponseDelete(DeleteView):
    template_name = 'delete_response.html'
    queryset = Advert.objects.all()
    success_url = '/adverts/'


class ResponseAccept(DetailView):
    pass

