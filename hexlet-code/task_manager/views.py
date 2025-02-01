from django.shortcuts import redirect, render

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

