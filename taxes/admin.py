from django.contrib import admin
from .models import Staff, Accruals_and_taxes
from django.contrib.auth.models import User


from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget 


class StaffResource(resources.ModelResource):
    author = fields.Field(column_name='author', attribute='author', widget=ForeignKeyWidget(User, 'username'))
    class Meta:
        model = Staff


@admin.register(Staff)
class StaffAdmin(ImportExportActionModelAdmin):
    resource_class = StaffResource
    list_display = [field.name for field in Staff._meta.fields if field.name !="id"]
    list_filter = ['surname', 'post', 'employment_date', 'author']
    search_fields = ['surname', 'post', 'employment_date', 'author']
    raw_id_fields = ['author']
    ordering = ['surname', 'post']
    def get_queryset(self, obj):
        return Staff.objects.all().order_by('surname')

#     list_display = ['author', 'id', 'surname', 'name', 'patronimic',

class Accruals_and_taxesResource(resources.ModelResource):
    worker = fields.Field(column_name='worker', attribute='worker', widget=ForeignKeyWidget(Staff, 'surname'))
    class Meta:
        model = Accruals_and_taxes

@admin.register(Accruals_and_taxes)
class Accruals_and_taxesAdmin(ImportExportActionModelAdmin):
    resource_class = Accruals_and_taxesResource
    # list_display = [field.name for field in Accruals_and_taxes._meta.fields if field.name !="id"]
    fields = ['worker', 'accrued', 'payment_date', 'reporting_date', 'description', 'alimony']
    list_display = ['worker', 'payment_date', 'accrued', 'social_deductions',
                    'alimony', 'alimony_tax', 'income_tax', 'salary', 'single_tax', 'injury_insurance', 'description', 'worker_id']

    def get_queryset(self, obj):
        return Accruals_and_taxes.objects.all().order_by('payment_date', '-worker')
    


    