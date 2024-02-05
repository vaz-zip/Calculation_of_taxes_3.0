from django.contrib import admin
from .models import Staff, Accruals_and_taxes

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget 

@admin.register(Staff)
class StaffAdmin(ImportExportActionModelAdmin):
    list_display = [field.name for field in Staff._meta.fields if field.name !="id"]





# @admin.register(Staff)
# class StaffAdmin(admin.ModelAdmin):
#     list_display = ['author', 'id', 'surname', 'name', 'patronimic',
#                     'post', 'ITN', 'employment_date', 'dependents', 'description']
#     list_filter = ['surname', 'post', 'employment_date', 'author']
#     search_fields = ['surname', 'post', 'employment_date', 'author']
#     raw_id_fields = ['author']
#     ordering = ['surname', 'post']
#     def get_queryset(self, obj):
#         return Staff.objects.all().order_by('surname')
    


@admin.register(Accruals_and_taxes)
class Accruals_and_taxesAdmin(admin.ModelAdmin):
    fields = ['worker', 'accrued', 'payment_date', 'reporting_date', 'description', 'alimony']
    list_display = ['worker', 'payment_date', 'accrued', 'social_deductions',
                    'alimony', 'alimony_tax', 'income_tax', 'salary', 'single_tax', 'injury_insurance', 'description', 'worker_id']

    def get_queryset(self, obj):
        return Accruals_and_taxes.objects.all().order_by('payment_date', '-worker')