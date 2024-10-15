from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *


urlpatterns = [
    #path('', cache_page(60*15)(costs_list), name='costs_list_url'),
    path('api/v1/reports/', ReportSerializerView.as_view(), name='report_list_url'),
    #path('days/<int:year>/<int:month>/<int:day>/',DayCostDetailView.as_view(),name='day_cost_detail_url'),
    path('api/v1/category_cost/create/', CategoryCostCreateView.as_view(), name='category_cost_create_url'),
    path('api/v1/category_cost/', CategoryCostListView.as_view(), name='category_cost_list_url'),
    path('api/v1/category_cost/<int:pk>/', CategoryCostDetailView.as_view(), name='category_cost_detail_url'),
    path('api/v1/category_cost/<int:pk>/update', CategoryCostUpdateView.as_view(), name='category_cost_update_url'),
    path('api/v1/category_cost/<int:pk>/delete', CategoryCostDeleteView.as_view(), name='category_cost_delete_url'),
    path('api/v1/costs/', CostListView.as_view(), name='costs_list_url'),
    path('api/v1/costs/<int:pk>/', CostDetailView.as_view(), name='cost_detail_url'),
    path('api/v1/costs/<int:pk>/update', CostUpdateView.as_view(), name='cost_update_url'),
    path('api/v1/costs/<int:pk>/delete', CostDeleteView.as_view(), name='cost_delete_url'),
    path('api/v1/costs/create/', CostCreateView.as_view(), name='cost_create_url'),
    
    path('api/v1/days/', DayCostListView.as_view(), name='day_cost_list_url'),
    path('api/v1/days/<int:year>/<int:month>/<int:day>/', DayCostDetailView.as_view(), name='day_cost_detail_url'),
    path('api/v1/days/<int:year>/<int:month>/<int:day>/update/', DayCostUpdateView.as_view(), name='day_cost_update_url'),
    path('api/v1/days/<int:year>/<int:month>/<int:day>/delete/', DayCostDeleteView.as_view(), name='day_cost_delete_url'),
    path('api/v1/days/create/', DayCostCreateView.as_view(), name='day_cost_create_url'),

    
    path('', cache_page(60*15)(main_costs_page), name='main_costs_page_url'),
    path('reports/', ReportCostView.as_view(), name='report_cost_url'),
    path('reports_add/', ReportAddMoneyView.as_view(), name='report_addmoney_url'),
    path('search/', SearchCostView.as_view(), name='search_cost_url'),
##    #path('days/<int:year>/<int:month>/<int:day>/',DayCostDetailView.as_view(),name='day_cost_detail_url'),
    path('category_cost/create/', CategoryCostCreateFrontView.as_view(), name='category_cost_front_create_url'),
    path('category_cost/', CategoryCostListFrontView.as_view(), name='category_cost_front_list_url'),
    path('category_cost/<int:pk>/', CategoryCostDetailFrontView.as_view(), name='category_cost_front_detail_url'),
    path('category_cost/<int:pk>/update', CategoryCostUpdateFrontView.as_view(), name='category_cost_front_update_url'),
    path('category_cost/<int:pk>/delete', CategoryCostDeleteFrontView.as_view(), name='category_cost_front_delete_url'),
    path('costs/', CostListFrontView.as_view(), name='costs_front_list_url'),
    path('costs/<int:pk>/', CostDetailFrontView.as_view(), name='cost_front_detail_url'),
    path('costs/<int:pk>/update', CostUpdateFrontView.as_view(), name='cost_front_update_url'),
    path('costs/<int:pk>/delete', CostDeleteFrontView.as_view(), name='cost_front_delete_url'),
    path('costs/create/', CostCreateFrontView.as_view(), name='cost_front_create_url'),
    path('costs/create/many/', CostManyCreateFrontView.as_view(), name='cost_many_front_create_url'),
    path('addmoney/', AddMoneyListFrontView.as_view(), name='addmoneys_front_list_url'),
    path('addmoney/<int:pk>/', AddMoneyDetailFrontView.as_view(), name='addmoney_front_detail_url'),
    path('addmoney/<int:pk>/update', AddMoneyUpdateFrontView.as_view(), name='addmoney_front_update_url'),
    path('addmoney/<int:pk>/delete', AddMoneyDeleteFrontView.as_view(), name='addmoney_front_delete_url'),
    path('addmoney/create/', AddMoneyCreateFrontView.as_view(), name='addmoney_front_create_url'),
    path('days/choice/', DayCostChoiceFrontView.as_view(), name='day_cost_choice_front_url'),
    path('days/', DayCostListFrontView.as_view(), name='day_cost_front_list_url'),
    path('days/<int:year>/<int:month>/<int:day>/<str:user>/', DayCostDetailFrontView.as_view(), name='day_cost_front_detail_url'),
    path('days/<int:year>/<int:month>/<int:day>/<str:user>/update/', DayCostUpdateFrontView.as_view(), name='day_cost_front_update_url'),
##    path('days/<int:year>/<int:month>/<int:day>/delete/', DayCostDeleteView.as_view(), name='day_cost_delete_url'),
##    path('days/create/', DayCostCreateView.as_view(), name='day_cost_create_url'),

   

]

