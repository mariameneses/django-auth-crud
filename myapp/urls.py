from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('hello/<str:username>', views.hello, name="hello"),
    # path('projects/', views.projects, name="projects"),
    # path('projects/<int:id>', views.project_detail, name="project_detail"),
    path('tasks/', views.tasks, name="tasks"),
    path('tasks/create_task/', views.create_task, name="create_task"),
    path('tasks/<int:task_id>', views.task_detail, name="task_detail"),
    path('tasks/<int:task_id>/complete', views.complete_task, name="complete_task"),
    path('tasks/<int:task_id>/delete', views.delete_task, name="delete_task"),
    # path('create_project/', views.create_project, name="create_project"),
    path('signup/', views.signup, name="sign_up"),
    path('logout/', views.signout, name="log_out"),
    path('signin/', views.signin, name="sign_in"),
] 