from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import  Task, Priority, DayPlan, CategoryTask, EveryDayTask

#admin.site.index_template = 'memcache_status/admin_index.html'


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display=('priority',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display=('user','name','category','description','date_to_do','priority','status')
    save_as=True
    save_on_top=True

@admin.register(DayPlan)
class DayPlanAdmin(admin.ModelAdmin):
    list_display=('user','day_date',)
    save_as=True
    save_on_top=True




@admin.register(CategoryTask)
class CategoryTaskAdmin(MPTTModelAdmin):
    list_display=('id','name','parent', 'user')
    save_as=True
    save_on_top=True

@admin.register(EveryDayTask)
class EveryDayTask(admin.ModelAdmin):
    list_display = ('id', 'body', 'date_everydaytask')


##@admin.register(Category)
##class CategoryAdmin(admin.ModelAdmin):
##    list_display=('id','name')
##
##@admin.register(TaskCategory)
##class TaskCategoryAdmin(admin.ModelAdmin):
##    list_display=('name',)
##
