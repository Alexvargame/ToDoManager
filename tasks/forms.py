from django import forms
from django.forms import widgets, fields

from .models import Task, DayPlan, CategoryTask, Priority

from datetime import datetime, date, time


class TaskForm(forms.ModelForm):

    category=forms.CharField(widget=forms.Select(choices=sorted([(obj.name,obj.name) for obj in CategoryTask.objects.all()]),attrs={'class':'form-control'}))

    class Meta:
        model=Task
        fields=['name','priority','date_create','date_to_do','description','status','remark','category']
        widgets={
            #'user':forms.TextInput(attrs={'class':'form-control', 'empty_value':True}),
            'name':forms.TextInput(attrs={'class':'form-control', 'empty_value':True}),
            'priority':forms.Select(choices=sorted([(obj.priority,obj.priority) for obj in Priority.objects.all()]),attrs={'class':'form-control'}),
            #'category':forms.Select(choices=sorted([(obj.name,obj.name) for obj in CategoryTask.objects.all()]),attrs={'class':'form-control'}),
            'date_create':forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}),
            'date_to_do':forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}),
            'description':forms.Textarea(attrs={'class':'form-control', 'empty_value':True}),
            'remark':forms.Textarea(attrs={'class':'form-control', 'empty_value':True}),
            'status':forms.Select(choices=[(True,True),(False,False)],attrs={'class':'form-control'}),
          
           }

##    def cleaned_date_to_do(self):
##        data=self.cleaned_data['date_to_do']
##        data_l=[int(i) for i in self.cleaned['date_to_do'].split('-')]
##        #data_range=(date(date_create_b[0],date_create_b[1],date_create_b[2])
##
##        if date(data_l[0],data_l[1],data_l[2])<date.today():
##            raise ValidatorError(_('Invalid date to do'))
##        return data
##        


class ChoiceDayForm(forms.Form):

    choice_day = forms.DateField(label='Выберите дату',widget=forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}))


class CreateDayForm(forms.ModelForm):
    class Meta:
        model=DayPlan
        fields=['day_date']
        widgets={
            'day_date':forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}),
            #'user':forms.TextInput(attrs={'class':'form-control', 'empty_value':True})#, 'disabled':True}),
           }


class CreateDayTasksForm(forms.Form):

    tasks = forms.CharField(label='Задания на выбор', required=False,
                          widget=forms.CheckboxSelectMultiple(choices=[(t.name,t.name) for t in Task.objects.all()],
                          attrs={'class':'form-control'}))

class EveryDayTaskForm(forms.Form):
    # body = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'empty_value':True}))
    # comment = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'empty_value':True}))
    body = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'empty_value':True}))
    comment = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'empty_value':True}))

class TaskSearchForm(forms.Form):
    
    #priorites=[(obj.priority,obj.priority) for obj in Priority.objects.all()]
    #name=forms.CharField(label='Название',max_length=100)
    category=forms.CharField(label='Категория',
                             widget=forms.CheckboxSelectMultiple(choices=sorted([(obj.name,obj.name) for obj in CategoryTask.objects.all()])))
    #description=models.CharField(label='Описание',max_length=500)
    #remark=models.CharField('Примечания',max_length=500,default='',blank=True)
    name = forms.CharField(label='Название')
    date_create_b=forms.DateField(label='начальная дата',widget=forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}))
    date_create_e=forms.DateField(label='конечная дата',widget=forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}))
    date_to_do_b=forms.DateField(label='начальная дата',widget=forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}))
    date_to_do_e=forms.DateField(label='конечная дата',widget=forms.DateInput(attrs={'class':'form-control', 'empty_value':True,'type':'date'}))
    priority=forms.CharField(label='Приоритет',widget=forms.CheckboxSelectMultiple(choices=sorted([(obj.priority,obj.priority) for obj in Priority.objects.all()])))
    status=forms.CharField(label="Статус исполнения",widget=forms.CheckboxSelectMultiple(choices=[(False,False),(True,True)]))


