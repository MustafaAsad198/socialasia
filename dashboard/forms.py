from django import forms
from .models import Profile,Predictmatch,Networkgraph,Caption,Examplecaption

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