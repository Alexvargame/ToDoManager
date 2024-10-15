from django import forms
from django.forms import widgets, fields

from django.contrib.auth.models import User


from .models import DayCost, CategoryCost, CategoryAddMoney




class  ChoiceDayForm(forms.Form):
   
    choice_day=forms.DateField(label='Выберите дату',widget=forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}))



class ReportCostForm(forms.Form):
    
    category=forms.CharField(label='Категория',
                             widget=forms.CheckboxSelectMultiple(choices=[(cat.id,cat.name) for cat in CategoryCost.objects.all()]))
                                         
    date_b=forms.DateField(label='начальная дата',widget=forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}))
    date_e=forms.DateField(label='конечная дата',widget=forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}))

  
class ReportAddMoneyForm(forms.Form):
  
    category=forms.CharField(label='Категория',
                             widget=forms.CheckboxSelectMultiple(choices=[(cat.id,cat.name) for cat in CategoryAddMoney.objects.all()]))
                                         
    date_b=forms.DateField(label='начальная дата',widget=forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}))
    date_e=forms.DateField(label='конечная дата',widget=forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}))


class CostManyCreateForm(forms.Form):

    user = forms.CharField(label='Пользователь',
                             widget=forms.Select(choices=[(us.id,us.username) for us in User.objects.all()],attrs={'class':'form-control', 'empty_value':True}))
    category = forms.CharField(label='Категория',
                             widget=forms.Select(choices=[(cat.id,cat.name) for cat in CategoryCost.objects.all()],attrs={'class':'form-control', 'empty_value':True}))
    cost_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'empty_value': True,'type': 'date'}))

class CostForm(forms.Form):

    cost_name = forms.CharField(label='Назначение',required=False, widget=forms.TextInput(attrs={'class':'form-control', 'empty_value':True},))
    cost_sum = forms.DecimalField(label='Сумма', initial=0.00, widget=forms.NumberInput(attrs={'class':'form-control', 'empty_value':True}))