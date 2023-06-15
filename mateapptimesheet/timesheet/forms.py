from django import forms
from .models import Company, Project, Time
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

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
            'timeType' : forms.TextInput(attrs={'class':'form-control','placeholder':'Type'}),
            'timeNotes': forms.Textarea(attrs={'class':'form-control','placeholder':'Notes','style':'height: 200px'}),
            'user': forms.Select(attrs={'class':'form-select'})
        }

    def __init__(self, *args, **kwargs):
        super(TimesheetForm, self).__init__(*args, **kwargs)
        
        self.fields['project'].queryset = Project.objects.filter(deleted=False).order_by('projectName')
        self.fields['project'].empty_label = _("Select Project:")

        self.fields['user'].queryset = get_user_model().objects.order_by('last_name')
        self.fields['user'].empty_label = _("Select User")