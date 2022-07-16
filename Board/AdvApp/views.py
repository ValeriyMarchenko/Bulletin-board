from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import *
from .forms import CreateAdvertForm, CreateResponseForm
from .filters import ResponseFilter

from django.shortcuts import redirect
from datetime import datetime
from django.views.generic.edit import FormMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


class AdvertList(ListView):
    model = Advert
    template_name = 'adverts.html'
    context_object_name = 'advertList'
    queryset = Advert.objects.order_by('-dateCreation')
    # paginate_by = 10


### if pagination is needed use this in .html ###

# {% if is_paginated %}
#     {% if page_obj.has_previous %}
#         <a href="?page=1">First</a>
#         <a href="?page={{ page_obj.previous_page_number }}"><<<</a>
#     {% endif %}

#     {% for num in page_obj.paginator.page_range %}
#         {% if page_obj.number == num %}
#             <a>{{ num }}</a>
#         {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
#             <a href="?page={{ num }}">{{ num }}</a>
#         {% endif %}
#     {% endfor %}

#     {% if page_obj.has_next %}
#         <a href="?page={{ page_obj.next_page_number }}">>>></a>
#         <a href="?page={{ page_obj.paginator.num_pages }}">End</a>
#     {% endif %}
# {% endif %}


class AdvertView(FormMixin, DetailView, LoginRequiredMixin):
    
    template_name = 'advert.html'
    form_class = CreateResponseForm
    context_object_name = 'advertView'
    queryset = Advert.objects.all()

    def post(self, request, *args, **kwargs):
        response = Response(
            id_user=request.user,
            id_advert=Advert.objects.get(pk=request.POST['id_advert']),
            text = request.POST.get('text', False),
        )
        response.save()

        user = response.id_advert.id_user

        html_content = render_to_string('mail_response.html', {'response': response, })

        mail_subject = f'Hi {user}. You have new response on your advert!'

        msg = EmailMultiAlternatives(
            subject=mail_subject,
            body='',
            from_email='s44tpdude@yandex.ru',
            to=[user.email],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return redirect('/')


class AdvertCreate(CreateView, LoginRequiredMixin):
    template_name = 'add.html'
    form_class = CreateAdvertForm

    def post(self, request, *args, **kwargs):
        advert = Advert(
            id_user=request.user,
            id_category=request.POST['category'],
            title = request.POST['title'],
            text=request.POST['text'],
            image = request.FILES.get('image', False),
            file=request.FILES.get('file', False)
        )
        advert.save()

        return redirect('/adverts/')


class AdvertUpdate(UpdateView, LoginRequiredMixin):
    template_name = 'edit.html'
    form_class = CreateAdvertForm
 
    
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Advert.objects.get(pk=id)

class AdvertDelete(DeleteView, LoginRequiredMixin):
    template_name = 'delete_advert.html'
    queryset = Advert.objects.all()
    success_url = '/adverts'


class ResponseList(ListView):
    model = Response
    template_name = 'responses.html'
    context_object_name = 'responseList'
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_adverts = Advert.objects.filter(id_user=self.request.user)
        query = Response.objects.filter(id_advert__in=user_adverts).order_by('-id_user')
        context['filter'] = ResponseFilter(self.request.GET, queryset=query)
        return context


class ResponseDelete(DeleteView):
    template_name = 'delete_response.html'
    queryset = Response.objects.all()
    success_url = '/adverts/responses'


class ResponseAccept(DetailView):
    model = Response
    template_name = 'accept_response.html'

    def post(self, request, *args, **kwargs):
        response = Response.objects.get(pk=request.POST['id_resp'])
        response.accepted = True
        response.save()

        return redirect('/adverts/responses')
