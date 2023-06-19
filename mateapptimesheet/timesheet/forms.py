from django import forms
from .models import Company, Project, Time
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

TYPE_CHOICES = [
    ("Business", _("Business Hours")),
    ("Non Business", _("Non Business Hours")),
]

FILTER_CHOICES = [
    (None, _("Select Filter")),
    ("Current_Month", _("Current Month")),
    ("Last_Month", _("Last Month")),
    ("Last_Trimester", _("Last Quarter")),
    ("Last_Semester", _("Last Semester")),
    ("Last_Year", _("Last Year"))
]

class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = [
            'companyName',
            'tax_id',
        ]

        widgets = {
            'companyName': forms.TextInput(attrs={'class':'form-control','placeholder':'Customer Name'}),
            'tax_id': forms.TextInput(attrs={'class':'form-control','placeholder':'Tax ID'}),
        }  

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = [
            'projectName',
            'company',
        ]
    
        widgets = {
            'projectName': forms.TextInput(attrs={'class':'form-control','placeholder':'Project Name'}),
            'company': forms.Select(attrs={'class':'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(deleted=False).order_by('companyName')
        self.fields['company'].empty_label = _("Select Customer:")

class TimesheetForm(forms.ModelForm):

    timeType = forms.ChoiceField(
        choices=TYPE_CHOICES
    )

    timeType.widget.attrs.update({'class': 'form-select'})

    class Meta:
        model = Time

        fields = [
            'timeItem',
            'timeDate',
            'project',
            'timeType',
            'timeNotes',
            'user',
        ]

        widgets = {
            'timeItem': forms.DateInput(attrs={'class':'form-control','placeholder':'Duration'}),
            'timeDate': forms.DateInput(attrs={'class':'form-control'}),
            'project': forms.Select(attrs={'class':'form-select'}),
            'timeNotes': forms.Textarea(attrs={'class':'form-control','placeholder':'Notes','style':'height: 200px'}),
            'user': forms.Select(attrs={'class':'form-select'})
        }

    def __init__(self, *args, **kwargs):
        super(TimesheetForm, self).__init__(*args, **kwargs)
        
        self.fields['project'].queryset = Project.objects.filter(deleted=False).order_by('projectName')
        self.fields['project'].empty_label = _("Select Project:")

        self.fields['user'].queryset = get_user_model().objects.order_by('last_name')
        self.fields['user'].empty_label = _("Select User")

class FilterForm(forms.Form):

    f = forms.ChoiceField(
        choices=FILTER_CHOICES,
        required=False,
    )
    f.widget.attrs.update({'class': 'form-select'})

    q = forms.CharField(
        label="Search",
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control me-2', 'placeholder':_('Search:'), 'type':'search', 'aria-label':'search'}),
    )