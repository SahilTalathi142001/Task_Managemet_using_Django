# tasks/views.py
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Project, Task

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    tasks = project.tasks.all()
    return render(request, 'project_detail.html', {'project': project, 'tasks': tasks})

def create_project(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        default_user = User.objects.get(username='Sahil')

        Project.objects.create(title=title, description=description, created_by=default_user)
        #Project.objects.create(title=title, description=description)
        return redirect('project_list')
    return render(request, 'create_project.html')

def create_task(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')
        Task.objects.create(title=title, description=description, project=project, assigned_to=assigned_to, due_date=due_date)
        return redirect('project_detail', project_id=project_id)
    return render(request, 'create_task.html', {'project': project})


def create_project(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        # Assuming projects are created by default by 'Anonymous' user
        created_by = 'Sahil'

        Project.objects.create(title=title, description=description, created_by=created_by)
        return redirect('project_list')
    return render(request, 'create_project.html')