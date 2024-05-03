from django.urls import path
from . import views
from .views import project_list



from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('projects/', views.project_list, name='project_list'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/new/', views.create_project, name='create_project'),
    path('project/<int:project_id>/task/new/', views.create_task, name='create_task'),
]


