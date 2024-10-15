from django.db import models
from django.shortcuts import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import datetime, date, time

class CategoryTask(MPTTModel):
    user=models.CharField(max_length=100, default='admin')
    #user = models.OneToOneField(User, on_delete=models.CASCADE)#, default=1)
    name=models.CharField(max_length=100)
    parent=TreeForeignKey(
        'self',
        related_name='children',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
        )
    class MPTTMeta:
        order_insertion_by=['name']
        verbose_name='Категория задания'
        verbose_name_plural='Категории заданий'

    def __str__(self):
        if self.parent==None:
            return f"{self.name}"
        else:
            return f"{self.parent}-{self.name}"

    def get_absolute_url(self):
        return reverse('category_detail_url',kwargs={'pk':self.id})

class Priority(models.Model):
    priority=models.CharField('Приоритет',max_length=30)

    class Meta:
        verbose_name='Приоритет'
        verbose_name_plural='Приоритеты'

    def __str__(self):
        return self.priority

    

class Task(models.Model):

    user=models.CharField(max_length=100, default='')
    name=models.CharField('Название', max_length=100)
    category=models.CharField('Категория', max_length=30, blank=True, null=True)
    description=models.CharField('Описание', max_length=2500)
    remark=models.CharField('Примечания', max_length=2500, default='', blank=True)
    date_create=models.DateTimeField('Дата создания')
    date_to_do=models.DateTimeField('Дата исполнения')
    priority=models.CharField('Приоритет', max_length=30)
    status=models.BooleanField("Статус исполнения", default=False)

    class Meta:
        verbose_name='Задание'
        verbose_name_plural='Задания'


   

    def __str__(self):
        return f"{self.user}-{self.name}"

    def get_absolute_url(self):
        return reverse('task_detail_url',kwargs={'pk':self.id})

    def get_update_url(self):
        return reverse('task_update_url',kwargs={'pk':self.id})

    def get_delete_url(self):
        return reverse('task_delete_url',kwargs={'pk':self.id})

    def get_remark(self):
        remark_list=self.remark.split('|')
        return remark_list



class DayPlan(models.Model):
    user=models.CharField(max_length=100, default='admin')
    day_date=models.DateField('День')
    tasks=models.ManyToManyField(Task,verbose_name="задания", related_name="day_tasks", blank=True)


    class Meta:
        verbose_name="Дневной план"
        verbose_name_plural="Дневные планы"

    def get_absolute_url(self):
        return reverse('day_detail_url',args=[self.day_date.year,self.day_date.month, self.day_date.day, self.user])#kwargs={'pk':self.id})
    def get_update_url(self):
        return reverse('day_update_url',args=[self.day_date.year,self.day_date.month, self.day_date.day, self.user])#kwargs={'pk':self.id})




