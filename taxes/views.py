from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from taxes.api.serializers import StaffSerializer, Accruals_and_taxesSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.db.models import Sum
# from django.urls import reverse
# from datetime import datetime
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Staff, Accruals_and_taxes
from .filters import StaffFilter, ChargesFilter, ReportFilter
from .forms import StaffCreateForm, ChargesCreateForm #StaffUpdateForm,
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint


def staff_pdf(request, staff_id):
        staff = get_object_or_404(Staff, id=staff_id)
        html = render_to_string('pdf.html', 
                                {'staff': staff},
                            )
        # html = HTML(string=html_string, base_url=request.build_absolute_uri())
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename={staff.id}_{staff.surname}.pdf'
        weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')])
        return response 

class StaffList(LoginRequiredMixin, ListView): 
    model = Staff
    template_name = 'staff.html'
    context_object_name = 'staff'
    queryset = Staff.objects.all()
    filter_class = StaffFilter
    paginate_by = 4

    def get_queryset(self):
        self.filter = self.filter_class(self.request.GET, super().get_queryset().filter(author_id=self.request.user.id))
        return self.filter.qs.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = StaffFilter(self.request.GET, queryset=self.get_queryset())
        return context
 

class StaffView(ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

class Accruals_and_taxesView(ModelViewSet):
    queryset = Accruals_and_taxes.objects.all()
    serializer_class = Accruals_and_taxesSerializer    


class StaffDetailView(LoginRequiredMixin, DetailView):
    model = Staff
    template_name = 'staff/employee.html'
    context_object_name = 'staff'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Staff.objects.get(pk=id)


class StaffCreateView(LoginRequiredMixin, CreateView):
    template_name = 'staff/staff_add.html'
    form_class = StaffCreateForm

    def get_success_url(self) -> str:
        return '/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            Staff.objects.create(**(form.cleaned_data) | {'author': request.user})
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)  
        

class StaffUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'staff/edit_staff.html'
    form_class = StaffCreateForm

    def get_object(self,  **kwargs):
        id = self.kwargs.get('pk')
        return Staff.objects.get(pk=id)
             
        
class StaffDeleteView(LoginRequiredMixin, DeleteView):
    model = Staff
    template_name = 'staff/delete_staff.html'
    context_object_name = 'staff'
    success_url = '/'        


class Pay_and_ChargesList(LoginRequiredMixin, ListView):
    model = Accruals_and_taxes
    template_name = 'pay_charges/pay_and_charges.html'
    context_object_name = 'accruals_and_taxes'
    filter_class = ChargesFilter
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['staff'] = Staff.objects.all()
        context['filter'] = ChargesFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        self.filter = self.filter_class(self.request.GET, super().get_queryset())
        return self.filter.qs.all()    

    
class СhargesDetailView(DetailView):
    model = Accruals_and_taxes
    template_name = 'pay_charges/charges_detail.html'
    context_object_name = 'accruals_and_taxes'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Accruals_and_taxes.objects.get(pk=id)    


class СhargesCreateView(LoginRequiredMixin, CreateView):
    template_name = 'pay_charges/charges_add.html'
    form_class = ChargesCreateForm

    def get_success_url(self) -> str:
        return '/charge'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            Accruals_and_taxes.objects.create(**(form.cleaned_data))  # | {'worker': request.user})
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)
        

class ChargesUpdateView(UpdateView):
    template_name = 'pay_charges/charges_edit.html'
    form_class = ChargesCreateForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Accruals_and_taxes.objects.get(pk=id)


class ChargesDeleteView(DeleteView):
    model = Accruals_and_taxes
    template_name = 'pay_charges/charge_delete.html'
    context_object_name = 'accruals_and_taxes'
    success_url = '/charge'


class FinreportList(LoginRequiredMixin, ListView):
    model = Accruals_and_taxes
    template_name = 'pay_charges/report.html'
    context_object_name = 'taxes'
    filter_class = ReportFilter
    

    def get_context_data(self, **kwargs):
        # self.filter = self.filter_class(self.request.GET, queryset=self.get_queryset())
        context = super().get_context_data(**kwargs)
        # context['staff'] = Staff.objects.all()
        context['filter'] = ReportFilter(self.request.GET, queryset=self.get_queryset())
        # c = self.request # получение запроса
        # print(c) # внешний вид запроса
        d = self.request.GET.get # получаем параметры запроса (ключ: знчение)
        # print(d)
        # print(d('start_date'))
        # print(d('end_date'))        
        start_date = d('start_date') # получаем переменную start_date
        end_date = d('end_date') # получаем переменную end_date
        processed_request = Accruals_and_taxes.objects.filter(reporting_date__range = (start_date, end_date)) # находим отфильтрованные по дате ключ: значение словаря QuerySet 
       
        def summ_accrued():
            summ = 0
            for item in processed_request.values('accrued'): # получаем начислеия за период
                for accrued in item.values():                
                    for i in [accrued]:                      # получаем сумму начислений за период
                        summ += i
            return summ
        context['summ'] = summ_accrued 

        def summ_social():
            summ = 0
            for item in processed_request:
                for i in [item.worker.dependents]:
                    if item.worker.dependents <= 2:
                        i = item.worker.dependents * 1400
                    elif item.worker.dependents >= 3:
                        i = (2800 + (3000 * int(item.worker.dependents - 2)))
                    else:
                        i = 0
                    summ += i
            return summ
        context['summ_social'] = summ_social   

        def summ_inc_tax():
            summ = 0
            for item in processed_request:
                for i in [item.worker.dependents]:
                    if item.worker.dependents <= 2:
                        i = (item.accrued - item.worker.dependents * 1400) * 0.13
                    elif item.worker.dependents >= 3:
                        i = (item.accrued - (2800 + (3000 * int(item.worker.dependents - 2)))) * 0.13
                    else:
                        i =  item.accrued * 0.13
                    summ += i
            return summ
        context['summ_inc_tax'] = summ_inc_tax

        def summ_salary():
            summ = 0
            for item in processed_request:
                for i in [item.worker.dependents]:
                    if item.worker.dependents <= 2:
                        i = item.accrued - (item.accrued - item.worker.dependents * 1400) * 0.13 - item.accrued * item.alimony * 0.01
                    elif item.worker.dependents >= 3:
                        i = item.accrued - (item.accrued - (2800 + (3000 * int(item.worker.dependents - 2)))) * 0.13 - item.accrued * item.alimony * 0.01
                    else:
                        i =  item.accrued - item.accrued * 0.13 - item.accrued * item.alimony * 0.01
                    summ += i
            return summ
        context['summ_salary'] = summ_salary

        def summ_alimony():
            summ = 0
            for item in processed_request:
                for i in [item.accrued * item.alimony * 0.01]:
                    summ += i
            return summ
        context['summ_al'] = summ_alimony  
        
        def sum_singl_tax():
            summ = 0
            for item in processed_request:
                for i in [item.accrued * 0.3]:
                    summ += i
            return summ
        context['summ_singl_tax'] = sum_singl_tax

        def sum_injury_insurance():
            summ = 0
            for item in processed_request:
                for i in [item.accrued * 0.004]:
                    summ += i
            return summ
        context['summ_injury_insurance'] = sum_injury_insurance

        return context
    
    def get_queryset(self):
        self.filter = self.filter_class(self.request.GET, super().get_queryset())
        return self.filter.qs.all()
         
