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
    ("Last_Year", _("Last Year")),
    ("All", _("All")),
]

HOUR_CHOICES = [
    (1, "1 Hs."),
    (2, "2 Hs."),
    (3, "3 Hs."),
    (4, "4 Hs."),
    (5, "5 Hs."),
    (6, "6 Hs."),
    (7, "7 Hs."),
    (8, "8 Hs."),
    (9, "9 Hs."),
    (10, "10 Hs."),
    (11, "11 Hs."),
    (12, "12 Hs."),
]

PROJECT_TYPE_CHOICES = [
    ("onetime", _("One-Time")),
    ("recurrent", _("Recurrent")),
]

PROJECT_STATUS_CHOICES = [
    (1, _("Active")),
    (0, _("Finished")),
]


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = [
            'companyName',
            'tax_id',
        ]

        widgets = {
            'companyName': forms.TextInput(attrs={'class':'form-control','required':'True','placeholder':'Customer Name'}),
            'tax_id': forms.TextInput(attrs={'class':'form-control','placeholder':'Tax ID'}),
        }  

class ProjectForm(forms.ModelForm):

    projectStatus = forms.ChoiceField(
        choices=PROJECT_STATUS_CHOICES
    )
    projectType = forms.ChoiceField(
        choices=PROJECT_TYPE_CHOICES
    )

    projectStatus.widget.attrs.update({'class': 'form-select'})
    projectType.widget.attrs.update({'class': 'form-select'})

    class Meta:
        model = Project
        fields = [
            'projectName',
            'company',
            'projectStatus',
            'projectType',
            'startDate',
            'budget',
            'projectNotes',
        ]
    
        widgets = {
            'projectName': forms.TextInput(attrs={'class':'form-control','required':'True','placeholder':'Project Name'}),
            'company': forms.Select(attrs={'class':'form-select','required':'True'}),
            'startDate' : forms.DateInput(attrs={'class':'form-control'}),
            'budget' : forms.NumberInput(attrs={'class':'form-control'}),
            'projectNotes': forms.Textarea(attrs={'class':'form-control','placeholder':'Notes','style':'height: 200px'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(deleted=False).order_by('companyName')
        self.fields['company'].empty_label = _("Select Customer:")

class TimesheetForm(forms.ModelForm):

    timeType = forms.ChoiceField(
        choices=TYPE_CHOICES
    )
    timeItem = forms.ChoiceField(
        choices=HOUR_CHOICES
    )

    timeType.widget.attrs.update({'class': 'form-select'})
    timeItem.widget.attrs.update({'class': 'form-select'})

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
            'timeDate': forms.DateInput(attrs={'class':'form-control','required':'True',}),
            # 'timeDate': forms.DateInput(attrs={'type':'date', 'class':'form-control'}),
            'project': forms.Select(attrs={'class':'form-select','required':'True',}),
            'timeNotes': forms.Textarea(attrs={'class':'form-control','placeholder':'Notes','style':'height: 200px'}),
            'user': forms.Select(attrs={'class':'form-select','required':'True'})
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