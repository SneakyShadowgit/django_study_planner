from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Subject, Task
from django.contrib.auth.models import User
from datetime import date
from datetime import datetime
from django.contrib.auth import logout

@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status=True).count()
    pending_tasks = tasks.filter(status=False).count()
    overdue_tasks = tasks.filter(status=False, deadline__lt=date.today()).count()

    completion = 0
    if total_tasks > 0:
        completion = (completed_tasks / total_tasks) * 100

    context = {
        'total': total_tasks,
        'completed': completed_tasks,
        'pending': pending_tasks,
        'overdue': overdue_tasks,
        'completion': completion,
        'tasks': tasks,
        'today': date.today(),
        'current_date': datetime.now(),
        'user_name': request.user.first_name + " " + request.user.last_name,
    }

    return render(request, 'dashboard.html', context)

from .forms import SubjectForm, TaskForm

@login_required
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            return redirect('dashboard')
    else:
        form = SubjectForm()
    return render(request, 'add_subject.html', {'form': form})


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})


@login_required
def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.status = True
    task.save()
    return redirect('dashboard')

@login_required
def logout_view(request):
    logout(request)
    return redirect('/admin/login/')