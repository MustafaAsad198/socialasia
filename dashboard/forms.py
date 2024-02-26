from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Profile,Predictmatch,Networkgraph,Caption,Examplecaption,Hub,HubDm,Meeting
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminSplitDateTime,AdminDateWidget,AdminTimeWidget


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location','pfp','age','sport','hobbies','gender','private']
    
class PredictDataFrom(forms.ModelForm):
    class Meta:
        model=Predictmatch
        fields=['user2']

class NetworkGraphPremiumForm(forms.ModelForm):
    class Meta:
        model=Networkgraph
        fields='__all__'
    
class NetworkGraphBoosterForm(forms.ModelForm):
    class Meta:
        model=Networkgraph
        fields=['level']

class CaptionForm(forms.ModelForm):
    class Meta:
        model=Caption
        fields='__all__'

class ExampleCaptionsForm(forms.ModelForm):
    class Meta:
        model=Examplecaption
        fields=['text', 'contentlength', 'obj']
        widgets={
            'summary':forms.Textarea(attrs={'rows':2})
        }

class HubCreateForm(forms.ModelForm):
    class Meta:
        model=Hub
        fields=['name','members']
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

