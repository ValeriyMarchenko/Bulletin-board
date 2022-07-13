from django import forms
from django.forms import ModelForm, TextInput
from .models import Advert, Response


class CreateAdvertForm(forms.ModelForm):
    category = forms.ChoiceField(label="Category", choices=Advert.CATEGORY, widget=forms.Select(attrs={"style": "width:100%"}))
    title = forms.CharField(label = 'Title', required = True)
    text = forms.CharField(label="Text", widget=forms.Textarea(attrs={"style": "width:100%"}))
    file = forms.FileField(label="File", required=False)
    image = forms.ImageField(label = 'Image', required = False)


    class Meta:
        model = Advert
        fields = ['category', 'title', 'text', 'file', 'image']


class CreateResponseForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = ['text', ]
        widgets = {'text': TextInput(attrs={'size': 100, 'placeholder': 'Enter your text here'})}

