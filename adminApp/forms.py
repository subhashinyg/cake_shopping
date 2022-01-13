from django import forms
from .models import *

class CakeImageForm(forms.ModelForm):
    class Meta:
        model = CakeImage
        fields = ['cake', 'image']
