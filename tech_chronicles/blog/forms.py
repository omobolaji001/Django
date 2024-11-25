""" Defines Form classes """
from django import forms


class EmailFormPost(forms.Form):
    """ Defines form for sharing posts through email """
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
