from django.shortcuts import render,redirect, reverse
from django.views.generic import View
from django.core.validators import MinValueValidator

from django import forms

from datetime import datetime, date, time
from django.contrib.auth.models import User
from users.models import Profile, PhoneNumber
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Task, DayPlan,CategoryTask,Priority
from .forms import TaskForm, ChoiceDayForm, CreateDayForm, CreateDayTasksForm, TaskSearchForm
from django.db.models import Q

def main_menu(request):
    return render(request,'tasks/main_page.html')

def task_list(request):
    tasks=Task.objects.filter(user=request.user.username)
    paginator=Paginator(tasks,15)
    page=request.GET.get('page')
    try:
        tasks=paginator.page(page)
    except PageNotAnInteger:
        tasks=paginator.page(1)
    except EmptyPage:
        tasks=paginator.page(paginator.num_pages)
        
    
    
    return render(request,'tasks/tasks_list.html',context={'page':page,'tasks':tasks})

def category_list(request):
    categories=CategoryTask.objects.filter(user=request.user.username)

    return render(request,'tasks/categories_list.html',context={'categories':categories})





class DayCreate(LoginRequiredMixin,View):

    def get(self, request):
       
        form=CreateDayForm(initial={'user':request.user.username})
        form_t=CreateDayTasksForm()
        return render(request,'tasks/create_day.html',context={'form':form, 'user':request.user.username,
            'tasks':form_t['tasks'].as_widget(forms.CheckboxSelectMultiple(choices=[(t.name,t.name) for t in Task.objects.filter(user=request.user.username,status=False,date_to_do__range=(date.today(),date(2025,1,1)))]))})
    def post(self,request):
       
        bound_form=CreateDayForm(request.POST,initial={'user':request.user.username})
        bound_form_t=CreateDayTasksForm(request.POST)
       
        date_b=[int(i) for i in request.POST['day_date'].split('-')]
        if DayPlan.objects.filter(user=request.user.username,day_date=date(date_b[0],date_b[1],date_b[2])).exists():# and DayPlan.objects.filter(user=request.user.username).exists():
            day=DayPlan.objects.get(user=request.user.username,day_date=date(date_b[0],date_b[1],date_b[2]))           
            return redirect(day) 
            
        if bound_form.is_valid():
            new_day=bound_form.save()
            new_day.tasks.set(Task.objects.filter(user=request.user.username,name__in=bound_form_t['tasks'].value()))
            new_day.user=request.user.username
            new_day.save()
            
            return redirect(new_day)
        else:
            return render(request,'tasks/create_day.html',context={'form':bound_form,'user':request.user.username,'s':(request.POST, request.user.username),
                            'tasks':bound_form_t['tasks'].as_widget(forms.CheckboxSelectMultiple(choices=[(t.name,t.name) for t in Task.objects.filter(user=request.user.username,status=False,date_to_do__range=(date.today(),date(2024,1,1)))]))})
            
class DayUpdate(LoginRequiredMixin,View):

    def get(self, request, year, month, day, user):
        day=DayPlan.objects.get(user=request.user.username,day_date__year=year,day_date__month=month,day_date__day=day)
        form_t=CreateDayTasksForm()

        task_choice=[(t.name,t.name) for t in Task.objects.filter(user=request.user.username,status=False,date_to_do__range=(date.today(),date(2025,1,1))) if t not in day.tasks.all()]
        return render(request,'tasks/update_day.html',context={'day':day,
            'tasks':form_t['tasks'].as_widget(forms.CheckboxSelectMultiple(choices=[(t.name,t.name) for t in Task.objects.filter(user=request.user.username,status=False,date_to_do__range=(date.today(),date(2025,1,1))) if t not in day.tasks.all()]))})
    def post(self,request, year, month, day, user):
        day=DayPlan.objects.get(user=request.user.username,day_date__year=year,day_date__month=month,day_date__day=day)
        bound_form_t=CreateDayTasksForm(request.POST)
        day_task=[t.name for t in day.tasks.all()]
        day_task.extend(bound_form_t['tasks'].value())
        
        if bound_form_t.is_valid():
            day.tasks.set(Task.objects.filter(user=request.user.username,name__in=day_task))
            day.save()
            return redirect(day)
        else:
            return render(request,'tasks/update_day.html',context={'day':day,'s':day_task,
             'tasks':bound_form_t['tasks'].as_widget(forms.CheckboxSelectMultiple(choices=[(t.name,t.name) for t in Task.objects.filter(user=request.user.username,status=False,date_to_do__range=(date.today(),date(2025,1,1))) if t not in day.tasks.all()]))})        
    

class ChoiceDay(LoginRequiredMixin,View):

    def get(self,request):
        form=ChoiceDayForm(initial={'choice_day':date.today()})
        return render(request,'tasks/choice_day.html',context={'form':form})

    def post(self,request):
        
        date_b=[int(i) for i in request.POST['choice_day'].split('-')]
        form=ChoiceDayForm(request.POST)
        if DayPlan.objects.filter(user=request.user.username,day_date=date(date_b[0],date_b[1],date_b[2])).exists():
            day=DayPlan.objects.get(user=request.user.username,day_date=date(date_b[0],date_b[1],date_b[2]))           
            return redirect(day)       
        else:
            return render(request,'tasks/choice_day.html',context={'form':form, 'info':f"Такой даты нет"})
    
class TaskDetailView(LoginRequiredMixin,View):

    def get(self,request,pk):
        task=Task.objects.get(id=pk)
       
        remark_list=task.remark.split('|')[:-1]

        return render(request,'tasks/task_detail.html',{'task':task, 'remark_list':remark_list})

    
class CategoryDetailView(LoginRequiredMixin,View):

    def get(self,request,pk):
        category=CategoryTask.objects.get(id=pk)
        task_list=Task.objects.filter(category=category.name)
        

        return render(request,'tasks/category_detail.html',{'category':category,'task_list':task_list})

class DayDetailView(LoginRequiredMixin,View):

    def get(self,request, year, month, day, user):
        day=DayPlan.objects.get(user=request.user.username,day_date__year=year,day_date__month=month,day_date__day=day)
        
        return render(request,'tasks/day_detail.html',{'day':day})


class TaskCreate(LoginRequiredMixin,View):
    def get(self,request):
        form=TaskForm(initial={'date_create': date.today(),'user':request.user.username})
        return render(request,'tasks/task_create.html',context={'form':form,
                'category':form['category'].as_widget(forms.Select(attrs={'class':'form-control'},choices=sorted([(obj.name,obj)for obj in CategoryTask.objects.filter(user=request.user.username)])))})

    def post(self,request):

        bound_form=TaskForm(request.POST,initial={'date_create': date.today(),'user':request.user.username})
        
        if bound_form.is_valid():
            date_to_do_l=[int(i) for i in request.POST['date_to_do'].split('-')]
            d=date.today()<=date(date_to_do_l[0],date_to_do_l[1],date_to_do_l[2])
            if date.today()<=date(date_to_do_l[0],date_to_do_l[1],date_to_do_l[2]):
                new_task=bound_form.save()
                new_task.remark=str(date.today())+':'+bound_form['remark'].value()+'|'
                new_task.user=request.user.username
                new_task.save()
                return redirect(new_task)
                #return render(request,'tasks/task_create.html',context={'form':bound_form,
                #'s':(request.POST['date_to_do'],date(date_to_do_l[0],date_to_do_l[1],date_to_do_l[2]),date.today(),d),
                #       'category':bound_form['category'].as_widget(forms.Select(attrs={'class':'form-control'},choices=sorted([(obj.name,obj)for obj in CategoryTask.objects.filter(user=request.user.username)])))})
    

            else:
                 return render(request,'tasks/task_create.html',context={'form':bound_form,'s':f"Проверьте введенные данные",
                       'category':bound_form['category'].as_widget(forms.Select(attrs={'class':'form-control'},choices=sorted([(obj.name,obj)for obj in CategoryTask.objects.filter(user=request.user.username)])))})
        else:
            return render(request,'tasks/task_create.html',context={'form':bound_form,'s':(request.POST),
                       'category':bound_form['category'].as_widget(forms.Select(attrs={'class':'form-control'},choices=sorted([(obj.name,obj)for obj in CategoryTask.objects.filter(user=request.user.username)])))})
    
class TaskSearch(LoginRequiredMixin,View):
     
    def get(self,request):
        priority_list=[]
        category_list=[]
        status_list=[]
        if request.GET:
            form=TaskSearchForm(request.GET,initial={'date_create_b': date(2023,1,1),'date_create_e': date(2024,1,1),
                                     'date_to_do_b': date(2023,1,1),'date_to_do_e': date(2024,1,1)})
            if form['category'].value():
                category_list=form['category'].value()
            else:
                for cat in CategoryTask.objects.filter(user=request.user.username):
                    category_list.append(cat.name)
            if form['priority'].value():
                priority_list=form['priority'].value()
            else:
                for pr in Priority.objects.all():
                    priority_list.append(pr.priority)
            if form['status'].value():
                status_list=form['status'].value()
            else:
                status_list=[False,True]

            name = form['name'].value()
            date_create_b=[int(i) for i in request.GET['date_create_b'].split('-')]
            date_create_e=[int(i) for i in request.GET['date_create_e'].split('-')]
            date_to_do_b=[int(i) for i in request.GET['date_to_do_b'].split('-')]
            date_to_do_e=[int(i) for i in request.GET['date_to_do_e'].split('-')]
    
            tasks = Task.objects.filter(
                Q(name__icontains=name.lower()) | Q(name__icontains=name.upper()) | Q(name__icontains=name.capitalize()),
                user=request.user.username,priority__in=priority_list, category__in=category_list, status__in=status_list,
                                     date_create__range=(date(date_create_b[0], date_create_b[1], date_create_b[2]), date(date_create_e[0], date_create_e[1], date_create_e[2])),
                                     date_to_do__range=(date(date_to_do_b[0], date_to_do_b[1], date_to_do_b[2]), date(date_to_do_e[0], date_to_do_e[1], date_to_do_e[2])))
            str_url=''
            for key, value in request.GET.items():
                str_url=str_url+key+'='+value+'&'
                
            paginator=Paginator(tasks,5)
            page_number=request.GET.get('page',1)
            page=paginator.get_page(page_number)

            is_paginated=page.has_other_pages()
            if page.has_previous():
                prev_url='?{}&page={}'.format(str_url[:-1],page.previous_page_number())
            else:
                prev_url=''

            if page.has_next():
                next_url='?{}&page={}'.format(str_url[:-1],page.next_page_number())
            else:
                next_url=''
##                
            return render(request,'tasks/task_search_list.html',context={'tasks':page,
                                                                    'is_paginated':is_paginated,
                                                                    'next_url':next_url,
                                                                    'prev_url':prev_url,
                                                                    's1':str_url[:-1],
                                                                    })
        

                
        else:
            form=TaskSearchForm(initial={'date_create_b': date(2023,1,1),'date_create_e': date(2024,1,1),
                                     'date_to_do_b': date(2023,1,1),'date_to_do_e': date(2024,1,1)})
            return render(request,'tasks/task_search.html',{'form':form,
                        'category':form['category'].as_widget(forms.CheckboxSelectMultiple(choices=sorted([(obj.name,obj.name)for obj in CategoryTask.objects.filter(user=request.user.username)])))})




  
class TaskUpdate(LoginRequiredMixin,View):
    def get(self,request,pk):
        
        task=Task.objects.get(id=pk)
        if task.remark is None:
            task_list=[]
        else:
            
            task_list=task.remark.split('|')[:-1]
        form=TaskForm(instance=task,initial={'remark':'','user':request.user.username})
        return render(request,'tasks/task_update.html',context={'form':form,'task_list':task_list,
            'category':form['category'].as_widget(forms.Select(attrs={'class':'form-control'},choices=sorted([(obj.name,obj.name)for obj in CategoryTask.objects.filter(user=request.user.username)])))})

    def post(self,request,pk):
        task=Task.objects.get(id=pk)
        str_remark=task.remark
        bound_form=TaskForm(request.POST,instance=task,initial={'remark':'','user':request.user.username})
        if bound_form.is_valid():
            new_task=bound_form.save()
            if bound_form['remark'].value()!='':
                new_task.remark=str_remark+str(date.today())+':'+bound_form['remark'].value()+'|'
            else:
                new_task.remark=str_remark
            new_task.save()
            return redirect(new_task)
        else:
            return render(request,'tasks/task_update.html',context={'form':bound_form,'task_list':task_list,'s':request.POST,
            'category':bound_form['category'].as_widget(forms.Select(attrs={'class':'form-control'},choices=sorted([(obj.name,obj.name)for obj in CategoryTask.objects.filter(user=request.user.username)])))})

class TaskDelete(LoginRequiredMixin,View):
    
    def get(self, request, pk):
        task=Task.objects.get(id=pk)
        return render(request, 'tasks/task_delete.html', context={'task':task})

     
    def post(self,request,pk):     
        task=Task.objects.get(id=pk)
        task.delete()
        return redirect(reverse('tasks_list_url'))
