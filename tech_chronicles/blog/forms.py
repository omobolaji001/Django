""" Defines Form classes """
from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    """ Defines form for sharing posts through email """
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    """ Defines a form for comments on blog posts """
    class Meta:
        """ metadata """
        model = Comment
        fields = ['name', 'email', 'body']
