from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Task, Company
from .forms import ProjectForm, TaskForm


def dashboard(request):

    if request.user.is_authenticated:
        company, created = Company.objects.get_or_create(
            owner=request.user,
            defaults={'name': f"{request.user.username}'s Company"}
        )
    else:
        # Guest (anonymous) user
        if 'company_id' not in request.session:
            company = Company.objects.create(
                name='Guest Company'
            )
            request.session['company_id'] = company.id
        else:
            company = Company.objects.get(
                id=request.session['company_id']
            )

    projects = Project.objects.filter(company=company)
    tasks = Task.objects.filter(company=company)

    context = {
        'projects': projects,
        'tasks': tasks,
        'total_projects': projects.count(),
        'completed_projects': projects.filter(status='completed').count(),
        'pending_tasks': tasks.exclude(status='done').count(),
        'project_status_counts': {
            'Planned': projects.filter(status='planned').count(),
            'Ongoing': projects.filter(status='ongoing').count(),
            'Completed': projects.filter(status='completed').count(),
        },
        'task_status_counts': {
            'To Do': tasks.filter(status='todo').count(),
            'In Progress': tasks.filter(status='progress').count(),
            'Done': tasks.filter(status='done').count(),
        },
    }

    return render(request, 'dashboard.html', context)



def project_list(request):
    company = get_current_company(request)
    projects = Project.objects.filter(company=company)
    return render(request, 'project_list.html', {'projects': projects})




def get_current_company(request):
    # Logged-in user
    if request.user.is_authenticated:
        company, _ = Company.objects.get_or_create(
            owner=request.user,
            defaults={'name': f"{request.user.username}'s Company"}
        )
        return company

    # Anonymous user (session-based)
    company_id = request.session.get('company_id')

    if company_id:
        return Company.objects.get(id=company_id)

    company = Company.objects.create(name='Guest Company')
    request.session['company_id'] = company.id
    return company





def project_add(request):
    company = get_current_company(request)

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



def project_delete(request, pk):
    company = get_object_or_404(Company, owner=request.user)
    project = get_object_or_404(Project, pk=pk, company=company)
    project.delete()
    return redirect('project_list')



def project_mark_complete(request, pk):
    company = get_object_or_404(Company, owner=request.user)
    project = get_object_or_404(Project, pk=pk, company=company)
    project.status = 'completed'
    project.save()
    return redirect('project_list')





def task_list(request):
    company = get_current_company(request)
    tasks = Task.objects.filter(company=company)
    return render(request, 'task_list.html', {'tasks': tasks})



def task_add(request):
    company = get_current_company(request)

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



def task_delete(request, pk):
    company = get_object_or_404(Company, owner=request.user)
    task = get_object_or_404(Task, pk=pk, company=company)
    task.delete()
    return redirect('task_list')



def task_mark_complete(request, pk):
    company = get_object_or_404(Company, owner=request.user)
    task = get_object_or_404(Task, pk=pk, company=company)
    task.status = 'done'
    task.save()
    return redirect('task_list')
