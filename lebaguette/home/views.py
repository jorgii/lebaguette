from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'home.html', locals())

def empty(requset):
    return HttpResponse(status=200)

