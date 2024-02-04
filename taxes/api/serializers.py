from rest_framework.serializers import ModelSerializer
from taxes.models import Staff, Accruals_and_taxes


class StaffSerializer(ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'author','surname', 'name', 'patronimic', 'ITN', 'post', 'dependents', 'employment_date', 'description']


class Accruals_and_taxesSerializer(ModelSerializer):
    class Meta:
        model = Accruals_and_taxes
        fields = ['worker', 'payment_date', 'reporting_date', 'accrued', 'social_deductions', 'alimony',
                  'alimony_tax','income_tax', 'salary', 'single_tax', 'injury_insurance', 'description'
                  ]
