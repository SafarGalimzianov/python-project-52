from django.shortcuts import redirect, render
from django.contrib import messages
import logging

def home(request):
    logger = logging.getLogger('django')
    logger.debug('Test debug log')
    return render (request, 'home.html')

class TaskPageView():
    ...

class TaskCreatePageView():
    ...

class TaskUpdatePageView():
    ...

class TaskDeletePageView():
    ...

