from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('Hello Django')
def test(request):
    return HttpResponse('This is test view!!!')
