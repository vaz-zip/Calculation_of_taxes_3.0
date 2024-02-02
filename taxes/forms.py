from django import forms
from .models import Staff, Accruals_and_taxes
from django.contrib.auth.models import User


class StaffCreateForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['surname', 'name', 'patronimic', 'post', 'ITN', 'dependents', 'description']


class ChargesCreateForm(forms.ModelForm):
    class Meta:
        model = Accruals_and_taxes
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'reporting_date': forms.DateInput(attrs={'type': 'date'}),
            }

        fields =[
            'worker', 'payment_date', 'reporting_date',
                'accrued', 'alimony', 'description']
     