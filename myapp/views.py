from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Project, Task
from .forms import CreateNewTask, CreateNewProject, TaskForm

# Create your views here.
def index(request):
    title = 'Django Course!!'
    return render(
        request, 'index.html', {'title': title}
    )

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                ) 
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Username already exists'
                    }
                )
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Password do not match'
            }
        )

@login_required
def signout(request):
    logout(request)
    return redirect('index')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{'form': AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            return render(request, 'signin.html',{
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
                }
            )
        else:
            login(request, user)
            return redirect('tasks')

def about(request):
    username = 'Majo aprende'
    return render(
        request, 'about.html',{'username':username}
    )

def hello(request, username):
    print('username:', username)
    return HttpResponse("<h1>Hello %s</h1>" % username)

@login_required
def projects(request):
    projects = Project.objects.all()
    return render(
        request, 'projects/projects.html', {'projects': projects}
    )

@login_required
def tasks(request):
    # task = get_object_or_404(Task, id=id)
    tasks_pending = Task.objects.filter(
        user=request.user, datecompleted__isnull=True
    )
    tasks_completed = Task.objects.filter(
        user=request.user, datecompleted__isnull=False
    ).order_by('-datecompleted')
    return render(
        request, 'tasks/tasks.html',{
        'tasks_pending': tasks_pending, 'tasks_completed': tasks_completed
        }
    )

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(
            request, 'tasks/create_task.html',{'form': CreateNewTask()}
        )
    else:
        try:
            print('request:', request.POST['title'])
            print('request:', request.POST['description'])
            Task.objects.create(
                title=request.POST['title'],
                description=request.POST['description'],
                project_id=1,
                user = request.user
            )
            return redirect('tasks')
        except:
            return render(
            request, 'tasks/create_task.html',{
                'form': CreateNewTask(), 'error': 'Please provide valid data'
            }
        )

@login_required
def task_detail(request,task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(
            request, 'tasks/task_detail.html', {'task': task, 'form': form}
        )
    else:
        try:
            form = TaskForm(request.POST, instance=task)
            print('form:', form)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(
                request, 'tasks/task_detail.html', {
                'task': task, 'form': form, 'error': "Error updating task"
                }
            )

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


@login_required
def create_project(request):
    if request.method == 'GET':
        return render(
            request,  'projects/create_project.html', {'form': CreateNewProject()}
        )
    else:
        Project.objects.create(name=request.POST['name'])
        return redirect('projects')

@login_required
def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    tasks = Task.objects.filter(project_id=id)
    return render(
        request, 'projects/detail.html', {'project': project, 'tasks': tasks}
    )
