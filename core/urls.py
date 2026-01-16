from django.urls import path
from . import views


from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Projects
    path('projects/', views.project_list, name='project_list'),
    path('projects/add/', views.project_add, name='project_add'),
    path('projects/edit/<int:pk>/', views.project_edit, name='project_edit'),
    path('projects/delete/<int:pk>/', views.project_delete, name='project_delete'),

    # Tasks
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/add/', views.task_add, name='task_add'),
    path('tasks/edit/<int:pk>/', views.task_edit, name='task_edit'),
    path('tasks/delete/<int:pk>/', views.task_delete, name='task_delete'),
    
    
    path('projects/complete/<int:pk>/', views.project_mark_complete, name='project_mark_complete'),
    path('tasks/complete/<int:pk>/', views.task_mark_complete, name='task_mark_complete'),
]
