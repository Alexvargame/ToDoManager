from django.contrib import admin

from .models import  DayCost, CategoryCost, Cost, AddMoney, CategoryAddMoney

@admin.register(CategoryCost)
class CategoryCostAdmin(admin.ModelAdmin):
    list_display=('id','name',)
     
@admin.register(CategoryAddMoney)
class CategoryAddMoneyAdmin(admin.ModelAdmin):
    list_display=('id','name',)
     
@admin.register(Cost)
class CostAdmin(admin.ModelAdmin):
    list_display=('id','user','category','cost_date','cost_name','cost_sum')
    save_as=True
    save_on_top=True

  
    

@admin.register(DayCost)
class DayCostAdmin(admin.ModelAdmin):
    list_display=('user','day_date','get_costs', 'get_day_sum')
    save_as=True
    save_on_top=True

@admin.register(AddMoney)
class AddMoneyAdmin(admin.ModelAdmin):
    list_display=('id','user','category','addmoney_date','addmoney_name','addmoney_sum')
    save_as=True
    save_on_top=True

   
