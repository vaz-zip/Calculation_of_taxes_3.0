from django.urls import path
from . import views
from .views import StaffList, StaffDetailView, StaffCreateView, StaffUpdateView, StaffDeleteView, Pay_and_ChargesList, СhargesDetailView, СhargesCreateView, \
                   ChargesDeleteView, ChargesUpdateView, FinreportList #  #doc_filter, , DocumentUpdateView, ImageDeleteView

from .models import Staff, Accruals_and_taxes

urlpatterns = [
    path('', StaffList.as_view(queryset=Staff.objects.all().order_by('surname'), template_name='staff/staff.html'), name='staff'),
    path('<int:pk>', StaffDetailView.as_view(), name='worker'),
    path('create', StaffCreateView.as_view(template_name='staff/staff_add.html'), name='staff_add'),
    path('staff_edit/<int:pk>', StaffUpdateView.as_view(), name='staff_edit'),
    path('staff_delete/<int:pk>', StaffDeleteView.as_view(), name='staff_delete'),
    path('charge', Pay_and_ChargesList.as_view(queryset=Accruals_and_taxes.objects.all().order_by('payment_date', 'worker')), name='charge'),
    path('charges/<int:pk>', СhargesDetailView.as_view(), name='charges'),
    path('char_create', СhargesCreateView.as_view(), name='char_add'),
    path('charge_edit/<int:pk>', ChargesUpdateView.as_view(), name='char_edit'),
    path('charge_delete/<int:pk>', ChargesDeleteView.as_view(), name='char_delete'),
    path('report', FinreportList.as_view(queryset=Accruals_and_taxes.objects.all().order_by('reporting_date', 'worker')), name='report'),
    path('<int:staff_id>/pdf/',views.staff_pdf, name='staff_pdf'),
]