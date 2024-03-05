from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User


class Staff(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Компания')
    surname = models.CharField(max_length=24, verbose_name='Фамилия')
    name = models.CharField(max_length=24, verbose_name='Имя')
    patronimic = models.CharField(max_length=24, blank=True, verbose_name='Отчество')
    ITN = models.PositiveBigIntegerField(unique=True, validators=[MaxValueValidator(999999999999)], verbose_name='ИНН')
    post = models.CharField(max_length=24, verbose_name='Должность')
    dependents = models.IntegerField(default=0, verbose_name='Иждивенцы')
    employment_date = models.DateField(null=True, verbose_name='Дата приёма')
    description = models.TextField(max_length=150, blank=True, verbose_name='Описание')

    class Meta:
        ordering = ['surname']
        indexes = [
            models.Index(fields=['surname']),
            ]
        verbose_name = 'Сотрудники'
        verbose_name_plural = 'Персонал'

    def __str__(self):
        return f'{self.surname} {self.name}'
    

    def get_absolute_url(self):
        return f'/{self.id}'

def default_datetime():
    return datetime.now()

class Accruals_and_taxes(models.Model):
    worker = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name='Работник')
    payment_date = models.DateField(verbose_name='Дата выплаты')
    reporting_date = models.DateField(verbose_name='Дата начисления', default=default_datetime, blank= True,null=True)
    accrued = models.FloatField(verbose_name='Начислено')
    social_ded = models.FloatField(default=0, verbose_name='Соц.вычет уч.')
    alimony = models.FloatField(default=0, verbose_name='Алименты в %')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return f'{self.worker}'

    class Meta:
        verbose_name = 'Начисления'

    def social_deductions(self):
        dependents = self.worker.dependents
        if dependents <= 2:
            return dependents * 1400
        elif dependents >= 3:
            return 2800 + (3000 * int(dependents - 2))
        else:
            return dependents == 0

    def income_tax(self):
        accrued = self.accrued
        social_ded = self.social_ded
        return (accrued - social_ded) * 0.13

    def alimony_tax(self):
        accrued = self.accrued
        alimony = self.alimony
        return accrued * alimony * 0.01

    def salary(self):
        accrued = self.accrued
        alimony_tax = self.alimony_tax()
        income_tax = self.income_tax()
        return accrued - (alimony_tax + income_tax)

    def single_tax(self):
        accrued = self.accrued
        return accrued * 0.3

    def injury_insurance(self):
        accrued = self.accrued
        return accrued * 0.004
    
    def __str__(self):
        return f'{self.accrued}'

    class Meta:
        verbose_name = 'Выплата'
        verbose_name_plural = 'Выплаты'

    def get_absolute_url(self):
        return f'/charges/{self.id}'

