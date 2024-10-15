from decimal import Decimal
from django.shortcuts import render, redirect
from django.views.generic import View
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.models import User

from .models import Cost, CategoryCost, DayCost


            
class ObjectCreateMixin:
    serializer=None
    template=None
    template_name = None
    model=None
   
    

    def get(self,request):
        serializer=self.serializer()
        return Response({'serializer':serializer})
        
    
    def post(self,request):

        serializer=self.serializer(data=request.data)
        if serializer.is_valid():            
            serializer.save()
            if self.model.__name__=="AddMoney":
                user=User.objects.get(id=request.data['user'])
                user.profile.balance=user.profile.balance+Decimal(request.data['addmoney_sum'])
                user.profile.save()
            if self.model.__name__=="Cost":
                user=User.objects.get(id=request.data['user'])
                user.profile.balance=user.profile.balance-Decimal(request.data['cost_sum'])
                user.profile.save()
                if DayCost.objects.filter(day_date=request.data['cost_date']).exists():
                    day=DayCost.objects.get(day_date=request.data['cost_date'])
                    cost_d=self.model.objects.filter(cost_date=request.data['cost_date'],user=user)
                    day.costs.set(cost_d)
                    day.save()
                else:
                    day=DayCost.objects.create(user=request.user.username,day_date=request.data['cost_date'])
                    cost_d=self.model.objects.filter(cost_date=request.data['cost_date'],user=user)
                    day.costs.set(cost_d)
                    day.save()
            return redirect(self.template)
        else:
            return Response({'serializer':serializer})

class ObjectsListMixin:
    serializer=None
    template_name = None
    model=None
    
    

    def get(self,request):
        objs=cache.get(self.model.__name__.lower())
        if not objs:
            objs=self.model.objects.all()
            cache.set(self.model.__name__.lower(),objs,10)
        paginator=Paginator(objs,15)
        page=request.GET.get('page')
        try:
            objs=paginator.page(page)
        except PageNotAnInteger:
            objs=paginator.page(1)
        except EmptyPage:
            objs=paginator.page(paginator.num_pages)
        
        serializer=self.serializer(objs,many=True)
        return Response({self.model.__name__.lower():objs, 'page':page})
        
class ObjectUpdateMixin:

    serializer=None
    template_name = None
    template = None
    model=None
    
    def get(self, request,pk):
        obj=self.model.objects.get(id=pk)
        serializer=self.serializer(obj)
        return Response({'serializer':serializer,self.model.__name__.lower()+'_update':obj})       
    def post(self,request,pk):     
        obj=self.model.objects.get(id=pk)
        if self.model.__name__=="Cost":
            sums=obj.cost_sum
        if self.model.__name__=="AddMoney":
            sums=obj.addmoney_sum
        serializer=self.serializer(obj,data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            if self.model.__name__=="Cost":
                request.user.profile.balance=request.user.profile.balance-Decimal(request.data['cost_sum'])+sums
                request.user.profile.save()
            if self.model.__name__=="AddMoney":
                #user=User.objects.get(username=request.user.username)
                request.user.profile.balance=request.user.profile.balance+Decimal(request.data['addmoney_sum'])-sums
                request.user.profile.save()
            return redirect(self.template)
        else:
            return Response({'serializer':serializer,self.model.__name__.lower()+'_update':objs})   

    
class ObjectDeleteMixin:

    template_name = None
    template= None
    model=None

    def get(self, request, pk):
        obj=self.model.objects.get(id=pk)
        return render(request, self.template_name, context={self.model.__name__.lower()+'_delete':obj})

     
    def post(self,request,pk):     
        obj=self.model.objects.get(id=pk)
        if self.model.__name__=="AddMoney":
                user=User.objects.get(username=obj.user)
                user.profile.balance=user.profile.balance-obj.addmoney_sum
                user.profile.save()
        if self.model.__name__=="Cost":
                user=User.objects.get(username=obj.user)
                user.profile.balance=user.profile.balance+obj.cost_sum
                user.profile.save()
        obj.delete()
        return redirect(reverse(self.template))

class ObjectDetailMixin:
    
    serializer=None
    template_name = None
    model=None
  

    def get(self, request,pk):
        key_detail=''
        obj=cache.get('object')
        if not obj:
            obj=self.model.objects.get(id=pk)
            cache.set('object',obj,10)
        else:
            
            if pk!=obj.id:
                key_detail='objects{}{}'.format(self.model.__name__.lower(),pk)
                obj=cache.get('key_detail')
                if not obj:
                    obj=self.model.objects.get(id=pk)
                    cache.set('key_detail',obj,20)
            
                
            
        serializer=self.serializer(obj)
        return Response({self.model.__name__.lower():obj})

##class ReportMixin:
##    form=None
##    template_name = None
##    model=None
##    model_category=None
##
##    def get(self, request):
##        category_list=[]
##        category_dict={}
##        date_dict={}
##        values_list=[]
##        new_values_list=[]
##        obj=self.model.__name__.lower()
##        objs=self.model.__name__.lower()+'s'
##        if request.GET:
##            form=self.form(request.GET,initial={'date_b':date(2023,5,1), 'date_e':date(2023,12,31)})
##            if form['category'].value():
##                category_list=form['category'].value()
##            else:
##                for cat in self.model_category.objects.all():
##                    category_list.append(str(cat.id))
##           
##            
##            objs=cache.get('report_'+objs)
##            
##            if not objs:
##                objs=self.model.objects.filter(user=request.user,
##                        category__in=[cat.id for cat in self.model_category.objects.filter(id__in=category_list)],
##                        obj+_date__range=(request.GET['date_b'],request.GET['date_e']))
##                cache.set('report'+_objs,objs,10)
##            else:
##                
##                values_list=([cat.id for cat in self.model_category.objects.filter(name__in=[obj.category for obj in objs])],
##                             min([obj.obj_date for obj in objs]),max([obj.obj_date for obj in objs]))
##                date_b_l=[int(i) for i in request.GET['date_b'].split('-')]
##                date_e_l=[int(i) for i in request.GET['date_e'].split('-')]
##                new_values_list=([int(c) for c in category_list],date(*date_b_l),date(*date_e_l))
##                if values_list!=new_values_list:
##                    key_rep='report_add_{}'.format(''.join([c for c in category_list])+''.join(str(d) for d in date_b_l)+''.join(str(d) for d in date_b_l))
##                    objs=cache.get(key_rep)
##                    if not objs:
##                        objs=self.model.objects.filter(user=request.user,
##                            category__in=[cat.id for cat in self.model_category.objects.filter(id__in=category_list)],
##                            obj_date__range=(request.GET['date_b'],request.GET['date_e']))
##                        cache.set(key_rep, objs,10)
##                        
##            
##            summary=sum([obj.obj_sum for obj in objs])
##            for obj in objs:
##                key,value=self.model_category.objects.get(name=obj.category),obj
##                l=category_dict.get(key,[])
##                l.append(value)
##                category_dict[key]=l
##
##            for key, value in category_dict.items():
##                value.append('Итого:{}'.format(sum([obj.obj_sum for obj in objs if obj.category==key])))
##                
##    
##            
##                
##            for obj in objs:
##                key,value=obj.obj_date,obj
##                l=date_dict.get(key,[])
##                l.append(value)
##                date_dict[key]=l
##            for key, value in date_dict.items():
##                value.append('Итого:{}'.format(sum([obj.obj_sum for obj in objs if obj.obj_date==key])))
##        
##            #summary_date=[sum([cost.cost_sum for cost in value]) for value in date_dict.values()]
##            
##        
##            context={
##                'form':form,
##                objs:objs,
##                'summary':summary,
##               # 'summary_period':sum(summary_period),
##                'category_dict':category_dict,
##                'date_dict':date_dict,
##
##               }
##            return render(request, 'costs/report_addmoney.html', context=context)
##        else:
##            form=self.form(initial={'date_b':date(2023,5,1), 'date_e':date(2023,12,31)})
##            return render(request, 'costs/report_addmoney.html', {'form':form})   
