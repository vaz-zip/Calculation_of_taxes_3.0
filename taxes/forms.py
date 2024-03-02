from django import forms
from .models import Staff, Accruals_and_taxes
from django.contrib.auth.models import User


class StaffCreateForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['surname', 'name', 'patronimic', 'post', 'ITN', 'dependents', 'description', 'employment_date']
        widgets = {
            'employment_date': forms.DateInput(attrs={'type': 'date'}),
            }


class ChargesCreateForm(forms.ModelForm):
    class Meta:
        model = Accruals_and_taxes
        widgets = {            
            'reporting_date': forms.DateInput(attrs={'type': 'date'}),
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            }

        fields =[
            'worker', 'reporting_date', 'payment_date', 
                'accrued', 'alimony', 'description']
     