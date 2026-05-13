from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-subject/', views.add_subject, name='add_subject'),
    path('add-task/', views.add_task, name='add_task'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('logout/', views.logout_view, name='logout'),
]

