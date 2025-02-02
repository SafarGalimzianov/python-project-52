from django.shortcuts import redirect, render
from django.contrib import messages

def home(request):
    return render (request, 'home.html')

class TaskPageView():
    ...

class TaskCreatePageView():
    ...

class TaskUpdatePageView():
    ...

class TaskDeletePageView():
    ...

