from django.shortcuts import render,get_object_or_404, redirect
from rest_framework.response import Response
from django.shortcuts import reverse
from django.views.generic import View

from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import formset_factory

from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.models import User
from datetime import date
from .models import DayCost,Cost, CategoryCost, AddMoney, CategoryAddMoney
from .forms import ChoiceDayForm, ReportCostForm, ReportAddMoneyForm, CostManyCreateForm,CostForm
from rest_framework.renderers import TemplateHTMLRenderer

from django.db.models import Q
from django.core.cache import cache

from .serializers import (CategoryCostCreateSerializer,
                          CategoryCostSerializer,
                          CostSerializer,
                          CostCreateSerializer,
                          DayCostSerializer,
                          DayCostCreateSerializer,
                          ReportSerializer,
                          CostDayUpdateSerializer,
                          DayCostUpdateSerializer,
                          AddMoneySerializer,
                          AddMoneyCreateSerializer)

from .utils import (ObjectCreateMixin,
                    ObjectsListMixin,
                    ObjectUpdateMixin,
                    ObjectDeleteMixin,
                    ObjectDetailMixin)

def costs_list(request):

    costs=Cost.objects.filter(user=request.user.id)
    return render(request, 'costs/costs_list.html', {'costs':costs})

def main_costs_page(request):

    
    return render(request, 'costs/main_costs_page.html')

def update_daycost():

    for cost in Cost.objects.all():
        
        if DayCost.objects.filter(day_date=cost.cost_date).exists():
            day=DayCost.objects.get(day_date=cost.cost_date)
            cost_d=self.model.objects.filter(cost_date=cost.cost_date,user=request.user)
            day.costs.set(cost_d)
            day.save()
        else:
            day=DayCost.objects.create(user=request.user.username,day_date=cost.cost_date)
            cost_d=self.model.objects.filter(id=cost[0].id)
            day.costs.set(cost_d)
            day.save()
    return redirect('costs/day_cost_list.html')



""" CRUD, List CategoryCost"""
class CategoryCostCreateView(LoginRequiredMixin,APIView):
    def post(self,request):

        serializer=CategoryCostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

class CategoryCostListView( LoginRequiredMixin,APIView):

    def get(self, request):
        categories=CategoryCost.objects.all()
        serializer=CategoryCostSerializer(categories,many=True)
        return Response(serializer.data)

class CategoryCostDetailView( LoginRequiredMixin,APIView):

    def get(self, request,pk):
        category=CategoryCost.objects.get(id=pk)
        serializer=CategoryCostSerializer(category)
        return Response(serializer.data)

class CategoryCostUpdateView(LoginRequiredMixin,APIView):
    
    def get(self, request,pk):
        category=CategoryCost.objects.get(id=pk)
        serializer=CategoryCostSerializer(category)
        return Response(serializer.data)       
    def post(self,request,pk):     
        category=CategoryCost.objects.get(id=pk)
        serializer=CategoryCostCreateSerializer(category,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)
        
class CategoryCostDeleteView( LoginRequiredMixin,APIView):

     def post(self,request,pk):     
        category=CategoryCost.objects.get(id=pk)
        category.delete()
        return Response(status=201)

""" CRUD, List Cost"""      
class CostListView( LoginRequiredMixin,APIView):

    def get(self, request):
        costs=Cost.objects.filter(user=request.user)
        serializer=CostSerializer(costs,many=True)
        return Response(serializer.data)

class CostDetailView( LoginRequiredMixin,APIView):

    def get(self, request,pk):
        cost=get_object_or_404(Cost,id=pk,user=request.user)
        serializer=CostSerializer(cost)
        return Response(serializer.data)
        
        
class CostCreateView(LoginRequiredMixin,APIView):
    def post(self,request):
        """ нужен свой валидатор для user, category"""
        
        serializer=CostCreateSerializer(data=request.data)
        if serializer.is_valid():
            cost=serializer.create(request.data)
            return Response(status=201)
        else:
            cost=serializer.create(request.data)
            if DayCost.objects.filter(day_date=request.data['cost_date']).exists():
                day=DayCost.objects.get(day_date=request.data['cost_date'])
                cost_d=Cost.objects.filter(cost_date=request.data['cost_date'],user=request.user)
                day.costs.set(cost_d)
                day.save()
            else:
                day=DayCost.objects.create(user=request.user.username,day_date=request.data['cost_date'])
                cost_d=Cost.objects.filter(id=cost[0].id)
                day.costs.set(cost_d)
                day.save()
            return Response(f' sum {day.get_day_sum()}')

class CostUpdateView(LoginRequiredMixin,APIView):

    def get(self, request,pk):
        cost=Cost.objects.get(id=pk,user=request.user)
        serializer=CostSerializer(cost)
        return Response(serializer.data)
    
    def post(self,request,pk):

        """ нужен свой валидатор для user, category"""
        cost=Cost.objects.get(id=pk,user=request.user)
        serializer=CostSerializer(cost,data=request.data)
        if serializer.is_valid():
            cost=serializer.save()
            return Response(status=201)
        else:
            cost=serializer.save()
            return Response(f'user {cost[0].user}, sum {cost[0].cost_sum}, cat- {cost[0].category}, date-{cost[0].cost_date}, name {cost[0].cost_name}')

class CostDeleteView( LoginRequiredMixin,APIView):

     def post(self,request,pk):     
        cost=Cost.objects.filter(id=pk,user=request.user)
        cost.delete()
        return Response(status=201)


""" CRUD, List DayCost"""

class DayCostListView( LoginRequiredMixin,APIView):

    def get(self, request):
        days=DayCost.objects.all()
        serializer=DayCostSerializer(days,many=True)
        return Response(serializer.data)

class DayCostDetailView( LoginRequiredMixin,APIView):

    def get(self, request, year, month, day):
        day=DayCost.objects.get(user=request.user.username,day_date__year=year,day_date__month=month,day_date__day=day)
        serializer=DayCostSerializer(day)
        return Response(serializer.data)

class DayCostCreateView(LoginRequiredMixin,APIView):
    def post(self,request):
        """ нужен свой валидатор для user, category"""
        
        serializer=DayCostCreateSerializer(data=request.data)
        if serializer.is_valid():
            day=serializer.create(request.data)
            costs=Cost.objects.filter(id__in=request.data['costs'])
            day[0].costs.set(costs)
            
            return Response(status=201)
        else:
            return Response(status=400)

class DayCostUpdateView(LoginRequiredMixin,APIView):

    def get(self, request, year, month, day):
        day=DayCost.objects.get(user=request.user.username,day_date__year=year,day_date__month=month,day_date__day=day)
        
        serializer=DayCostSerializer(day)
        return Response(serializer.data)

    
    def post(self,request, year, month, day):
        """ нужен свой валидатор для user, category"""
        day=DayCost.objects.get(user=request.user.username,day_date__year=year,day_date__month=month,day_date__day=day)
        serializer=DayCostCreateSerializer(day,data=request.data)
  
        if serializer.is_valid():
            day=serializer.save()
            costs=Cost.objects.filter(id__in=request.data['costs'])
            day.costs.set(costs)
            
            return Response(status=201)
        else:
            return Response(status=400)
                
class DayCostDeleteView(LoginRequiredMixin,APIView):

     def post(self,request,year, month, day):     
        day=DayCost.objects.get(user=request.user.username,day_date__year=year,day_date__month=month,day_date__day=day)
        day.delete()
        return Response(status=201)

class ReportSerializerView(LoginRequiredMixin,APIView):

  
    def post(self, request):
        
        costs=Cost.objects.filter(user=request.user, category__in=[cat.id for cat in CategoryCost.objects.filter(id__in=request.data['category'])], cost_date__range=(request.data['date_b'],request.data['date_e']))
        serializer=CostSerializer(costs,many=True)
        summary=sum([cost.cost_sum for cost in costs])
        context={'Расходы за период по категориям':serializer.data,'Итого':summary}
        return Response(context)


""" Frontend"""

""" CRUD, List DayCost"""
class DayCostChoiceFrontView( LoginRequiredMixin,APIView):
    def get (self, request):
        form = ChoiceDayForm(initial={'choice_day':date.today()})
        return render(request,'costs/choice_day.html',context={'form':form})
    def post (self, request):
        date_b = [int(i) for i in request.POST['choice_day'].split('-')]
        form = ChoiceDayForm(request.POST)
        if DayCost.objects.filter(user=request.user.username,day_date=date(date_b[0],date_b[1],date_b[2])).exists():
            day = DayCost.objects.get(user=request.user.username,day_date=date(date_b[0],date_b[1],date_b[2]))
            #return render(request,'costs/choice_day.html',context={'form':form, 'info':f"Такой даты нет",'s':day})
            return redirect(day)       
        else:
            return render(request,'costs/choice_day.html',context={'form':form, 'info':f"Такой даты нет"})

class DayListFrontView(ObjectsListMixin,LoginRequiredMixin,APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'costs/day_cost_list.html'
    serializer=DayCostSerializer
    model=DayCost

class DayCostDetailFrontView(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'costs/day_cost_detail.html'

    def get(self,request, year, month, day, user):
        daycost=DayCost.objects.get(user=request.user.username,day_date__year=year,day_date__month=month,day_date__day=day)
        serializer=DayCostSerializer(daycost)
        return Response({'daycost':daycost})

##class DayCostUpdateFrontView(LoginRequiredMixin,APIView):
##
##    renderer_classes = [TemplateHTMLRenderer]
##    template_name = 'costs/day_cost_update.html'
##    
##    def get(self, request, year, month, day, user):
##        daycost=DayCost.objects.get(user=request.user.username,day_date__year=year,day_date__month=month,day_date__day=day)
##        serializer=DayCostSerializer(daycost)
##        return Response({'serializer':serializer,'daycost':daycost})       
##    def post(self,request, year, month, day, user):     
##        daycost=DayCost.objects.get(user=request.user.username,day_date__year=year,day_date__month=month,day_date__day=day)
##        serializer=DayCostCreateSerializer(daycost,data=request.data)
##        if serializer.is_valid():
##            serializer.save()
##            return redirect('category_cost_front_list_url')
##        else:
##            return Response({'serializer':serializer,'daycost':daycost})
    
class DayCostUpdateFrontView(LoginRequiredMixin,APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'costs/day_cost_update.html'
    
    def get(self, request, year, month, day, user):
        daycost=DayCost.objects.get(user=request.user.username,day_date__year=year,day_date__month=month,day_date__day=day)
        query=[(c.cost_name,c.cost_name) for c in daycost.costs.all()]
        serializer=DayCostUpdateSerializer(daycost)
        return Response({'serializer':serializer,'daycost':daycost,
                        's':(query,daycost)})
##    def post(self,request, year, month, day, user):
##        daycost=DayCost.objects.get(user=request.user.username,day_date__year=year,day_date__month=month,day_date__day=day)
##        serializer=DayCostCreateSerializer(daycost,data=request.data)
##        if serializer.is_valid():
##            serializer.save()
##            return redirect('category_cost_front_list_url')
##        else:
##            return Response({'serializer':serializer,'daycost':daycost})

class DayCostListFrontView( LoginRequiredMixin,ObjectsListMixin,APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'costs/day_cost_list.html'
    serializer=DayCostSerializer
    model=DayCost

    
""" CRUD, List CategoryCost"""
class CategoryCostCreateFrontView(LoginRequiredMixin,ObjectCreateMixin, APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'costs/category_cost_create.html'
    template = 'category_cost_front_list_url'
    serializer = CategoryCostCreateSerializer
    model=CategoryCost

   

class CategoryCostListFrontView( LoginRequiredMixin,ObjectsListMixin,APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'costs/category_cost_list.html'
    serializer = CategoryCostSerializer
    model = CategoryCost



class CategoryCostDetailFrontView(ObjectDetailMixin,LoginRequiredMixin,APIView):

    serializer = CategoryCostSerializer
    model = CategoryCost
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'costs/category_cost_detail.html'

class CategoryCostUpdateFrontView(ObjectUpdateMixin,LoginRequiredMixin,APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'costs/category_cost_update.html'
    template = 'category_cost_front_list_url'
    serializer = CategoryCostSerializer
    model = CategoryCost
    

    
class CategoryCostDeleteFrontView(ObjectDeleteMixin,LoginRequiredMixin,APIView):

    template_name = 'costs/category_cost_delete.html'
    template = 'category_cost_front_list_url'
    model = CategoryCost



""" CRUD, List Cost"""

class CostCreateFrontView(LoginRequiredMixin,ObjectCreateMixin, APIView):
    serializer = CostCreateSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'costs/cost_create.html'
    template = 'costs_front_list_url'
    model = Cost


class CostManyCreateFrontView(LoginRequiredMixin, APIView):

    def get(self, request):
        form = CostManyCreateForm(initial={'cost_date':date.today()})
        SectionFormset = formset_factory(CostForm, extra=4)
        formset = SectionFormset()
        return render(request, 'costs/cost_many_create.html', {'form': form, 'formset': formset})
    def post(self, request):
        bound_form = CostManyCreateForm(request.POST, initial={'cost_date': date.today()})
        SectionFormset = formset_factory(CostForm, extra=4)
        bound_formset = SectionFormset(request.POST)
        if bound_form.is_valid() and bound_formset.is_valid():
            user = User.objects.get(id=bound_form['user'].value())
            category = CategoryCost.objects.get(id=bound_form['category'].value())
            cost_date = bound_form['cost_date'].value()
            summ=0
            for form in bound_formset:
                if form['cost_name'].value()!='':
                    new_cost = Cost.objects.create(user=user, category=category, cost_date=cost_date,
                                                   cost_name=form['cost_name'].value(),
                                                   cost_sum=form['cost_sum'].value())
                    print(form['cost_sum'].value(), type(form['cost_sum'].value()))
                    summ +=Decimal(form['cost_sum'].value())
            #user = User.objects.get(id=request.data['user'])
            user.profile.balance = user.profile.balance - Decimal(summ)
            user.profile.save()
            if DayCost.objects.filter(day_date=request.POST['cost_date']).exists():
                day = DayCost.objects.filter(day_date=request.POST['cost_date'])[0]
                cost_d = Cost.objects.filter(cost_date=request.POST['cost_date'], user=user)
                day.costs.set(cost_d)
                day.save()
            else:
                day = DayCost.objects.create(user=request.user.username, day_date=request.POST['cost_date'])
                cost_d = Cost.objects.filter(cost_date=request.POST['cost_date'], user=user)
                day.costs.set(cost_d)
                day.save()
            return redirect('costs_front_list_url')
        else:
            return render(request, 'costs/cost_many_create.html', {'form': bound_form, 'formset': bound_formset})


class CostListFrontView(LoginRequiredMixin,ObjectsListMixin,APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'costs/costs_list.html'
    serializer=CostSerializer
    model = Cost



class CostDetailFrontView(ObjectDetailMixin,LoginRequiredMixin,APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'costs/cost_detail.html'
    serializer=CostSerializer
    model = Cost





class CostUpdateFrontView(ObjectUpdateMixin,LoginRequiredMixin,APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'costs/cost_update.html'
    template= 'costs_front_list_url'
    serializer=CostSerializer
    model=Cost

   
class CostDeleteFrontView(ObjectDeleteMixin,LoginRequiredMixin,APIView):

    template_name = 'costs/cost_delete.html'
    template= 'costs_front_list_url'
    model=Cost


""" CRUD, List AddMoney"""

class AddMoneyCreateFrontView(LoginRequiredMixin,ObjectCreateMixin, APIView):
    serializer=AddMoneyCreateSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'costs/addmoney_create.html'
    template='addmoneys_front_list_url'
    model=AddMoney

class AddMoneyListFrontView(LoginRequiredMixin,ObjectsListMixin,APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'costs/addmoneys_list.html'
    serializer=AddMoneySerializer
    model=AddMoney

class AddMoneyDetailFrontView(ObjectDetailMixin,LoginRequiredMixin,APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'costs/addmoney_detail.html'
    serializer=AddMoneySerializer
    model=AddMoney

class AddMoneyUpdateFrontView(ObjectUpdateMixin,LoginRequiredMixin,APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'costs/addmoney_update.html'
    template= 'addmoneys_front_list_url'
    serializer=AddMoneySerializer
    model=AddMoney

   
class AddMoneyDeleteFrontView(ObjectDeleteMixin,LoginRequiredMixin,APIView):

    template_name = 'costs/addmoney_delete.html'
    template= 'addmoneys_front_list_url'
    model=AddMoney



""" Reports """
class ReportCostView(LoginRequiredMixin,APIView):

    def get(self, request):
        category_list=[]
        category_dict={}
        date_dict={}
        values_list=[]
        new_values_list=[]

        if request.GET:
            form=ReportCostForm(request.GET,initial={'date_b':date(2023,5,1), 'date_e':date(2023,12,31)})
            if form['category'].value():
                category_list=form['category'].value()
            else:
                for cat in CategoryCost.objects.all():
                    category_list.append(str(cat.id))
            costs=cache.get('report')
            if not costs:
                costs=Cost.objects.filter(user=request.user,
                        category__in=[cat.id for cat in CategoryCost.objects.filter(id__in=category_list)],
                        cost_date__range=(request.GET['date_b'],request.GET['date_e']))
                cache.set('report',costs,10)
            else:
                values_list=([cat.id for cat in CategoryCost.objects.filter(name__in=[cost.category for cost in costs])],
                             min([cost.cost_date for cost in costs]),max([cost.cost_date for cost in costs]))
                date_b_l=[int(i) for i in request.GET['date_b'].split('-')]
                date_e_l=[int(i) for i in request.GET['date_e'].split('-')]
                new_values_list=([int(c) for c in category_list],date(*date_b_l),date(*date_e_l))
                if values_list!=new_values_list:
                    key_rep='report_{}'.format(''.join([c for c in category_list])+''.join(str(d) for d in date_b_l)+''.join(str(d) for d in date_b_l))
                    costs=cache.get(key_rep)
                    if not costs:
                        costs=Cost.objects.filter(user=request.user,
                            category__in=[cat.id for cat in CategoryCost.objects.filter(id__in=category_list)],
                            cost_date__range=(request.GET['date_b'],request.GET['date_e']))
                        cache.set(key_rep, costs,10)
            summary=sum([cost.cost_sum for cost in costs])
            for cost in costs:
                key,value=CategoryCost.objects.get(name=cost.category),cost
                l=category_dict.get(key,[])
                l.append(value)
                category_dict[key]=l
            for key, value in category_dict.items():
                value.append('Итого:{}'.format(sum([cost.cost_sum for cost in costs if cost.category==key])))
            for cost in costs:
                key,value=cost.cost_date,cost
                l=date_dict.get(key,[])
                l.append(value)
                date_dict[key]=l
            for key, value in date_dict.items():
                value.append('Итого:{}'.format(sum([cost.cost_sum for cost in costs if cost.cost_date==key])))
        
            context={
                'form':form,
                'costs':costs,
                'summary':summary,
                'category_dict':category_dict,
                'date_dict':date_dict,

               }
            return render(request, 'costs/report.html', context=context)
        else:
            form=ReportCostForm(initial={'date_b':date(2023,5,1), 'date_e':date(2023,12,31)})
            return render(request, 'costs/report.html', {'form':form})   

class ReportAddMoneyView(LoginRequiredMixin,APIView):
    def get(self, request):
        category_list=[]
        category_dict={}
        date_dict={}
        values_list=[]
        new_values_list=[]
        if request.GET:
            form=ReportAddMoneyForm(request.GET,  initial={'date_b':date(2023,5,1), 'date_e':date(2023,12,31)})
            if form['category'].value():
                category_list=form['category'].value()
            else:
                for cat in CategoryAddMoney.objects.all():
                    category_list.append(str(cat.id))
            addmoneys=cache.get('report_add')
            if not addmoneys:
                addmoneys = AddMoney.objects.filter(user=request.user,
                        category__in=[cat.id for cat in CategoryAddMoney.objects.filter(id__in=category_list)],
                        addmoney_date__range=(request.GET['date_b'],request.GET['date_e']))
                cache.set('report_add',addmoneys,10)
            else:
                
                values_list=([cat.id for cat in CategoryAddMoney.objects.filter(name__in=[addmoney.category for addmoney in addmoneys])],
                             min([addmoney.addmoney_date for addmoney in addmoneys]),max([addmoney.addmoney_date for addmoney in addmoneys]))
                date_b_l=[int(i) for i in request.GET['date_b'].split('-')]
                date_e_l=[int(i) for i in request.GET['date_e'].split('-')]
                new_values_list=([int(c) for c in category_list],date(*date_b_l),date(*date_e_l))
                if values_list!=new_values_list:
                    key_rep='report_add_{}'.format(''.join([c for c in category_list])+''.join(str(d) for d in date_b_l)+''.join(str(d) for d in date_b_l))
                    addmoneys=cache.get(key_rep)
                    if not addmoneys:
                        addmoneys=AddMoney.objects.filter(user=request.user,
                            category__in=[cat.id for cat in CategoryAddMoney.objects.filter(id__in=category_list)],
                            addmoney_date__range=(request.GET['date_b'],request.GET['date_e']))
                        cache.set(key_rep, addmoneys,10)
 
            summary=sum([addmoney.addmoney_sum for addmoney in addmoneys])
            for addmoney in addmoneys:
                key,value=CategoryAddMoney.objects.get(name=addmoney.category),addmoney
                l=category_dict.get(key,[])
                l.append(value)
                category_dict[key]=l

            for key, value in category_dict.items():
                value.append('Итого:{}'.format(sum([addmoney.addmoney_sum for addmoney in addmoneys if addmoney.category==key])))
            for addmoney in addmoneys:
                key,value=addmoney.addmoney_date,addmoney
                l=date_dict.get(key,[])
                l.append(value)
                date_dict[key]=l
            for key, value in date_dict.items():
                value.append('Итого:{}'.format(sum([addmoney.addmoney_sum for addmoney in addmoneys if addmoney.addmoney_date==key])))
            context={
                'form':form,
                'addmoneys':addmoneys,
                'summary':summary,
                'category_dict':category_dict,
                'date_dict':date_dict,

               }
            return render(request, 'costs/report_addmoney.html', context=context)
        else:
            form=ReportAddMoneyForm(initial={'date_b':date(2023,5,1), 'date_e':date(2023,12,31)})
            return render(request, 'costs/report_addmoney.html', {'form':form})   

class SearchCostView(LoginRequiredMixin,APIView):

    def get(self, request):
       
        qs=request.GET.get('search','')
        url ='?page={}'.format(qs)
        costs=Cost.objects.filter(Q(cost_name__icontains=qs.lower())|Q(cost_name__icontains=qs.upper())|Q(cost_name__icontains=qs.capitalize()))
        summary=sum([cost.cost_sum for cost in costs])
        
        return render(request, 'costs/report_list.html', {'costs':costs,'summary':summary})

