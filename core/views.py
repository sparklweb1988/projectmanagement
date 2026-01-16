from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Task, Company
from .forms import ProjectForm, TaskForm



@login_required
def dashboard(request):
    company, created = Company.objects.get_or_create(
        owner=request.user,
        defaults={'name': f"{request.user.username}'s Company"}
    )

    projects = Project.objects.filter(company=company)
    tasks = Task.objects.filter(company=company)

    # Chart data
    project_status_counts = {
        'Planned': projects.filter(status='planned').count(),
        'Ongoing': projects.filter(status='ongoing').count(),
        'Completed': projects.filter(status='completed').count(),
    }

    task_status_counts = {
        'To Do': tasks.filter(status='todo').count(),
        'In Progress': tasks.filter(status='progress').count(),
        'Done': tasks.filter(status='done').count(),
    }

    context = {
        'projects': projects,
        'tasks': tasks,
        'total_projects': projects.count(),
        'completed_projects': projects.filter(status='completed').count(),
        'pending_tasks': tasks.exclude(status='done').count(),
        'project_status_counts': project_status_counts,
        'task_status_counts': task_status_counts,
    }

    return render(request, 'dashboard.html', context)




def project_list(request):
    company = get_object_or_404(Company, owner=request.user)
    projects = Project.objects.filter(company=company)

    return render(request, 'project_list.html', {'projects': projects})




def project_add(request):
    company = get_object_or_404(Company, owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.company = company
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'project_form.html', {'form': form, 'title': 'Add Project'})




@login_required
def project_edit(request, pk):
    company = get_object_or_404(Company, owner=request.user)
    project = get_object_or_404(Project, pk=pk, company=company)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project_form.html', {'form': form, 'title': 'Edit Project'})



@login_required
def project_delete(request, pk):
    company = get_object_or_404(Company, owner=request.user)
    project = get_object_or_404(Project, pk=pk, company=company)
    project.delete()
    return redirect('project_list')
   






def task_list(request):
    company = get_object_or_404(Company, owner=request.user)
    tasks = Task.objects.filter(company=company)

    return render(request, 'task_list.html', {'tasks': tasks})



@login_required
def task_add(request):
    company = get_object_or_404(Company, owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.company = company
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form, 'title': 'Add Task'})




@login_required
def task_edit(request, pk):
    company = get_object_or_404(Company, owner=request.user)
    task = get_object_or_404(Task, pk=pk, company=company)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form, 'title': 'Edit Task'})




@login_required
def task_delete(request, pk):
    company = get_object_or_404(Company, owner=request.user)
    task = get_object_or_404(Task, pk=pk, company=company)
    task.delete()
    return redirect('task_list')




@login_required
def project_mark_complete(request, pk):
    company = get_object_or_404(Company, owner=request.user)
    project = get_object_or_404(Project, pk=pk, company=company)
    project.status = 'completed'
    project.save()
    return redirect('project_list')

@login_required
def task_mark_complete(request, pk):
    company = get_object_or_404(Company, owner=request.user)
    task = get_object_or_404(Task, pk=pk, company=company)
    task.status = 'done'
    task.save()
    return redirect('task_list')
