from django import forms
from django.utils.translation import gettext_lazy as _

class SearchForm(forms.Form):
    q = forms.CharField(
        label="Search",
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control me-2', 'placeholder':_('Search:'), 'type':'search', 'aria-label':'search'}),
    )