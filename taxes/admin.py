from django.contrib import admin
from .models import Staff, Accruals_and_taxes


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['author', 'id', 'surname', 'name', 'patronimic',
                    'post', 'ITN', 'employment_date', 'dependents', 'description']
    list_filter = ['surname', 'post', 'employment_date', 'author']
    search_fields = ['surname', 'post', 'employment_date', 'author']
    raw_id_fields = ['author']
    ordering = ['surname', 'post']
    def get_queryset(self, obj):
        return Staff.objects.all().order_by('surname')
    


@admin.register(Accruals_and_taxes)
class Accruals_and_taxesAdmin(admin.ModelAdmin):
    fields = ['worker', 'accrued', 'payment_date', 'reporting_date', 'description', 'alimony']
    list_display = ['worker', 'payment_date', 'accrued', 'social_deductions',
                    'alimony', 'alimony_tax', 'income_tax', 'salary', 'single_tax', 'injury_insurance', 'description', 'worker_id']

    def get_queryset(self, obj):
        return Accruals_and_taxes.objects.all().order_by('payment_date', '-worker')