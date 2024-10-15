from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date, time
from django.shortcuts import reverse

class CategoryCost(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name="Категория расходов"
        verbose_name_plural="Категории расходов"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_cost_front_detail_url',kwargs={'pk':self.id})
    def get_update_url(self):
        return reverse('category_cost_front_update_url',kwargs={'pk':self.id})
    def get_delete_url(self):
        return reverse('category_cost_front_delete_url',kwargs={'pk':self.id})
    def get_cat_costs(self):
        costs_dict={}
        for cost in Cost.objects.filter(category=self.id):
            key, value=cost.id,cost.cost_sum
            costs_dict[key]=value        
        return costs_dict

    def get_sum_for_category(self):
        return sum(cost.cost_sum for cost in Cost.objects.filter(category=self.id))

class CategoryAddMoney(models.Model):
    name=models.CharField(max_length=100)
    class Meta:
        verbose_name="Категория поступлений"
        verbose_name_plural="Категории поступлений"

    def __str__(self):
        return self.name

##    def get_absolute_url(self):
##        return reverse('category_cost_front_detail_url',kwargs={'pk':self.id})
##    def get_update_url(self):
##        return reverse('category_cost_front_update_url',kwargs={'pk':self.id})
##    def get_delete_url(self):
##        return reverse('category_cost_front_delete_url',kwargs={'pk':self.id})
    def get_cat_addmoneys(self):
        addmoneys_dict={}
        for addmoney in AddMoney.objects.filter(category=self.id):
            key, value=addmoney.id,addmoney.addmoney_sum
            addmoneys_dict[key]=value        
        return addmoneys_dict

    def get_sum_for_category(self):
        return sum(addmoney.addmoney_sum for addmoney in AddMoney.objects.filter(category=self.id))


class Cost(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь',related_name='cost_creator', on_delete=models.DO_NOTHING, null=True, blank=True)
    category = models.ForeignKey(CategoryCost, verbose_name='Категория', related_name="category_cost", on_delete=models.DO_NOTHING)
    cost_date = models.DateField(verbose_name='День')
    cost_name = models.CharField(verbose_name='Назначение', max_length=1000,blank=True)
    cost_sum = models.DecimalField(verbose_name='Сумма', max_digits=10, decimal_places=2)

    class Meta:
        
        verbose_name="Расход"
        verbose_name_plural="Расходы"

    def get_absolute_url(self):
        return reverse('cost_front_detail_url',kwargs={'pk':self.id})
    def get_update_url(self):
        return reverse('cost_front_update_url',kwargs={'pk':self.id})
    def get_delete_url(self):
        return reverse('cost_front_delete_url',kwargs={'pk':self.id})

    
    def __str__(self):
        
        return f'{self.cost_name}-{self.cost_sum}'
   

class DayCost(models.Model):
    user = models.CharField(verbose_name='Пользователь', max_length=100, default='admin')
    day_date = models.DateField(verbose_name='День')
    costs = models.ManyToManyField(Cost, verbose_name="Расходы", related_name="day_costs", blank=True)

    class Meta:
        verbose_name = "Дневной расход"
        verbose_name_plural = "Дневные расходы"

    def get_absolute_url(self):
        return reverse('day_cost_front_detail_url',args=[self.day_date.year,self.day_date.month, self.day_date.day, self.user])

    def get_update_url(self):
        return reverse('day_cost_front_update_url',args=[self.day_date.year,self.day_date.month, self.day_date.day, self.user])
    
    def get_costs(self):
        costs_dict={}
        for cost in self.costs.all():
            key, value=cost.cost_name,cost.cost_sum
            costs_dict[key]=value
            
        return costs_dict
    
    def get_day_sum(self):
        return sum(self.get_costs().values())

    

    def __str__(self):
         return f'день - {self.day_date}'

class AddMoney(models.Model):

    user=models.ForeignKey(User, related_name='addmoney_creator',
                            on_delete=models.DO_NOTHING, null=True,blank=True)
    category=models.ForeignKey(CategoryAddMoney,verbose_name='Категория',related_name="category_addmoney", on_delete=models.DO_NOTHING)
    addmoney_date=models.DateField('День')#, default='')
    addmoney_name=models.CharField('Инфо',max_length=1000,blank=True)
    addmoney_sum=models.DecimalField('Сумма',max_digits=10, decimal_places=2)

    class Meta:
        
        verbose_name="Поступление"
        verbose_name_plural="Поступления"

    def get_absolute_url(self):
        return reverse('addmoney_front_detail_url',kwargs={'pk':self.id})
    def get_update_url(self):
        return reverse('addmoney_front_update_url',kwargs={'pk':self.id})
    def get_delete_url(self):
        return reverse('addmoney_front_delete_url',kwargs={'pk':self.id})

    
    def __str__(self):
        
        return f'{self.addmoney_name}-{self.addmoney_sum}'
   
