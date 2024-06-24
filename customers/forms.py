from django.contrib.auth.forms import UserCreationForm
from .models import Customer
from django import forms


class AccountOpeningForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['email', 'first_name', 'last_name', 'phonenumber', 'password1', 'password2']

class OrderTrackingForm(forms.Form):
    tracking_number = forms.CharField(max_length=100)

class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['email', 'first_name', 'last_name', 'phonenumber']