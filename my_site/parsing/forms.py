from django import forms

from .models import *


class SearchForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), to_field_name='slug', required=False,
        label='Город', widget=forms.Select(attrs={'class': 'form-control'}))
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(), to_field_name='slug', required=False,
        label='Язык программирования', widget=forms.Select(attrs={'class': 'form-control'}))


class GlobalSearchForm(forms.Form):
    keyword = forms.CharField(label='Ключевое слово',
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    save_keyword = forms.BooleanField(required=False,
                                      widget=forms.CheckboxInput,
                                      label='Сохранить результат поиска?')
