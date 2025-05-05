from django import forms
from django.contrib.auth.models import User
from .models import Items

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150,help_text="")
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'password_confirm']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class ItemForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ['call_sign', 'aircraft_type', 'detail', 'origin', 'destination', 'action','time', 'timeliness', 'remarks']

        labels = {
            'time': 'Time (UTC)',  
        }

    

