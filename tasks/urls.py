from django.urls import path

from .views import *


urlpatterns = [
    path('', main_menu, name='main_menu_url'),
    path('tasks/',task_list,name='tasks_list_url'),
    path('categories/',category_list,name='categories_list_url'),
    path('categories/<int:pk>/',CategoryDetailView.as_view(),name='category_detail_url'),
    path('tasks/<int:pk>/',TaskDetailView.as_view(),name='task_detail_url'),
    path('tasks/create/',TaskCreate.as_view(),name='task_create_url'),
    path('tasks/search/',TaskSearch.as_view(),name='task_search_url'),
    path('tasks/<int:pk>/update/',TaskUpdate.as_view(),name='task_update_url'),
    path('tasks/<int:pk>/delete', TaskDelete.as_view(), name='task_delete_url'),
    path('days',ChoiceDay.as_view(),name='choice_day_url'),
    path('days/create',DayCreate.as_view(),name='create_day_url'),
    path('days/update/<int:year>/<int:month>/<int:day>/<str:user>/',DayUpdate.as_view(),name='day_update_url'),
    path('days/<int:year>/<int:month>/<int:day>/<str:user>/',DayDetailView.as_view(),name='day_detail_url'),

]

