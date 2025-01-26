from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

def index(request):
    return render(request, 'fulfillX/index.html')