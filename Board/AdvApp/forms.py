from django import forms

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
    text = forms.CharField(label="Text", widget=forms.Textarea(attrs={"style": "width:100%"}))


    class Meta:
        model = Response
        fields = ['text']